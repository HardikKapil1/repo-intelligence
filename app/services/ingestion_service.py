# app/services/ingestion_service.py
from dataclasses import replace
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
from app.ingestion.safe_parser import safe_parse_python
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
        """
        Index a GitHub repository.

        Current flow:

        Repository
            ↓
        Clone
            ↓
        Discover files
            ↓
        Filter files
            ↓
        Detect language
            ↓
        Classify file
            ↓
        Parse supported code
            ↓
        Generate chunks
            ↓
        Persist chunks
        """

        repository = self.db.get(
            Repository,
            repository_id,
        )

        if repository is None:
            raise ValueError("Repository not found")

        print(
            f"[INGESTION] Starting repository: {repository_id}",
            flush=True,
        )

        repository.status = RepositoryStatus.INDEXING
        self.db.commit()

        try:
            # ---------------------------------------------------------
            # 1. Clone repository
            # ---------------------------------------------------------

            print(
                "[INGESTION] Cloning repository...",
                flush=True,
            )

            repository_path = self.cloner.clone(
                repository.github_url,
                repository.id,
            )

            print(
                f"[INGESTION] Repository cloned: {repository_path}",
                flush=True,
            )

            # ---------------------------------------------------------
            # 2. Discover files
            # ---------------------------------------------------------

            discovered_files = self.discovery.discover(repository_path)

            print(
                f"[INGESTION] Discovered files: {len(discovered_files)}",
                flush=True,
            )

            # ---------------------------------------------------------
            # 3. Filter files
            # ---------------------------------------------------------

            filtered_files = self.file_filter.filter(discovered_files)

            print(
                f"[INGESTION] Accepted files: {len(filtered_files.accepted)}",
                flush=True,
            )

            print(
                f"[INGESTION] Filtered files: {len(filtered_files.filtered)}",
                flush=True,
            )

            # ---------------------------------------------------------
            # 4. Process accepted files
            # ---------------------------------------------------------

            print(
                "[INGESTION] Starting file processing",
                flush=True,
            )

            for index, source_file in enumerate(
                filtered_files.accepted,
                start=1,
            ):
                print(
                    f"[FILE {index}/{len(filtered_files.accepted)}] "
                    f"{source_file.relative_path}",
                    flush=True,
                )

                self._process_file(
                    source_file=source_file,
                    repository_id=repository.id,
                )

                print(
                    f"[DONE] {source_file.relative_path}",
                    flush=True,
                )

            # ---------------------------------------------------------
            # 5. Finish ingestion
            # ---------------------------------------------------------

            print(
                "[INGESTION] ALL FILES PROCESSED",
                flush=True,
            )

            repository.status = RepositoryStatus.READY

            print(
                "[DB] COMMIT START",
                flush=True,
            )

            self.db.commit()

            print(
                "[DB] COMMIT DONE",
                flush=True,
            )

            print(
                f"[INGESTION] Repository {repository_id} READY",
                flush=True,
            )

        except Exception as exc:
            print(
                f"[INGESTION] FAILED: {exc}",
                flush=True,
            )

            self.db.rollback()

            # Refresh repository because rollback expires ORM state.
            repository = self.db.get(
                Repository,
                repository_id,
            )

            if repository is not None:
                repository.status = RepositoryStatus.FAILED
                self.db.commit()

            raise

    def _process_file(
        self,
        source_file,
        repository_id: UUID,
    ) -> None:
        """
        Process one repository file.

        This function intentionally separates:

            detection
            classification
            persistence
            parsing

        so each stage has one responsibility.
        """

        # -------------------------------------------------------------
        # 1. Detect language
        # -------------------------------------------------------------

        detected_language = self.language_detector.detect(source_file.path)

        # SourceFile is immutable, therefore create a new object.
        source_file = replace(
            source_file,
            language=detected_language,
        )

        print(
            f"  [LANGUAGE] {source_file.relative_path} → {detected_language}",
            flush=True,
        )

        # -------------------------------------------------------------
        # 2. Classify file
        # -------------------------------------------------------------

        category = self.classifier.classify(source_file)

        print(
            f"  [CATEGORY] {source_file.relative_path} → {category.value}",
            flush=True,
        )

        # -------------------------------------------------------------
        # 3. Save repository file metadata
        # -------------------------------------------------------------

        repository_file = RepositoryFile(
            repository_id=repository_id,
            path=str(source_file.relative_path),
            language=detected_language,
            category=category.value,
            size_bytes=source_file.size_bytes,
        )

        self.db.add(repository_file)

        # We need the generated repository_file.id
        # before creating child chunks.
        self.db.flush()

        # -------------------------------------------------------------
        # 4. Parse supported code
        # -------------------------------------------------------------

        if category == FileCategory.CODE and detected_language == "python":
            self._process_python_file(
                source_file=source_file,
                repository_file=repository_file,
            )

    def _process_python_file(
        self,
        source_file,
        repository_file: RepositoryFile,
    ) -> None:
        """
        Parse a Python source file and persist semantic chunks.
        Parsing runs in an isolated subprocess so a tree-sitter
        C-level crash cannot take down the whole ingestion run.
        """

        print(
            f"    [START PYTHON] {source_file.relative_path}",
            flush=True,
        )

        # -------------------------------------------------------------
        # 1. Read source
        # -------------------------------------------------------------

        source = source_file.path.read_text(
            encoding="utf-8",
            errors="replace",
        )

        print(
            f"    [READ] {len(source)} characters",
            flush=True,
        )

        # -------------------------------------------------------------
        # 2. Parse AST (isolated subprocess)
        # -------------------------------------------------------------

        status, result = safe_parse_python(source)

        if status != "ok":
            print(
                f"    [PARSE FAILED] {source_file.relative_path} → {status}: {result}",
                flush=True,
            )
            # Skip this file's chunks but let the rest of ingestion continue.
            return

        # Narrow the parser result for type checkers; failed parses return a
        # diagnostic string while successful parses return CodeSymbol objects.
        if isinstance(result, str):
            print(
                f"    [PARSE FAILED] {source_file.relative_path} → {result}",
                flush=True,
            )
            return

        symbols = result

        print(
            f"    [PARSED] {len(symbols)} symbols",
            flush=True,
        )

        # -------------------------------------------------------------
        # 3. Generate semantic chunks
        # -------------------------------------------------------------

        chunks = self.chunker.chunk(
            symbols=symbols,
            file_path=source_file.relative_path,
            language="python",
        )

        print(
            f"    [CHUNKED] {len(chunks)} chunks",
            flush=True,
        )

        # -------------------------------------------------------------
        # 4. Persist chunks
        # -------------------------------------------------------------

        for chunk in chunks:
            # Skip any chunk with corrupted line numbers (defense
            # against tree-sitter node metadata corruption).
            if (
                chunk.start_line < 1
                or chunk.end_line < chunk.start_line
                or chunk.start_line > 10_000_000
            ):
                print(
                    f"    [SKIP CORRUPT] {chunk.symbol_name} "
                    f"start={chunk.start_line} end={chunk.end_line}",
                    flush=True,
                )
                continue

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
