from hashlib import sha256
from pathlib import Path
from uuid import UUID

from sqlalchemy.orm import Session

from app.ingestion.chunking import CodeChunker
from app.ingestion.classification import FileCategory, FileClassifier
from app.ingestion.filesystem import FileDiscovery
from app.ingestion.filter import FileFilter
from app.ingestion.github import GitHubCloner
from app.ingestion.language import LanguageDetector
from app.ingestion.parsers.python import PythonParser
from app.models.chunk import Chunk
from app.models.enums import RepositoryStatus
from app.models.repository import Repository
from app.models.repository_file import RepositoryFile


class IngestionService:
    def __init__(self, db: Session) -> None:
        self.db = db

        self.cloner = GitHubCloner(Path("data/repositories"))
        self.discovery = FileDiscovery()
        self.file_filter = FileFilter()
        self.language_detector = LanguageDetector()
        self.classifier = FileClassifier()
        self.python_parser = PythonParser()
        self.chunker = CodeChunker()

    def index_repository(self, repository_id: UUID) -> None:
        repository = self.db.get(Repository, repository_id)

        if repository is None:
            raise ValueError("Repository not found")

        repository.status = RepositoryStatus.INDEXING
        self.db.commit()

        try:
            repository_path = self.cloner.clone(
                repository.github_url,
                repository.id,
            )

            discovered_files = self.discovery.discover(repository_path)
            filtered_files = self.file_filter.filter(discovered_files)

            for source_file in filtered_files.accepted:
                detected_language = self.language_detector.detect(source_file.path)

                category = self.classifier.classify(source_file)

                repository_file = RepositoryFile(
                    repository_id=repository.id,
                    path=str(source_file.relative_path),
                    language=detected_language,
                    category=category.value,
                    size_bytes=source_file.size_bytes,
                )

                self.db.add(repository_file)
                self.db.flush()

                if category == FileCategory.CODE and source_file.language == "python":
                    self._process_python_file(
                        source_file=source_file,
                        repository_file=repository_file,
                    )

            repository.status = RepositoryStatus.READY
            self.db.commit()

        except Exception:
            self.db.rollback()

            repository.status = RepositoryStatus.FAILED
            self.db.commit()

            raise

    def _process_python_file(
        self,
        source_file,
        repository_file: RepositoryFile,
    ) -> None:
        source = source_file.path.read_text(
            encoding="utf-8",
            errors="replace",
        )

        symbols = self.python_parser.parse(source)

        chunks = self.chunker.chunk(
            symbols=symbols,
            file_path=source_file.relative_path,
            language="python",
        )

        for chunk in chunks:
            content_hash = sha256(chunk.content.encode("utf-8")).hexdigest()

            db_chunk = Chunk(
                repository_file_id=repository_file.id,
                symbol_name=chunk.symbol_name,
                symbol_type=chunk.symbol_type,
                parent_symbol=chunk.parent_symbol,
                content=chunk.content,
                content_hash=content_hash,
                start_line=chunk.start_line,
                end_line=chunk.end_line,
            )

            self.db.add(db_chunk)
