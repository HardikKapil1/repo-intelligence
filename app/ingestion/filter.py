# app/ingestion/filter.py
from dataclasses import dataclass, field
from pathlib import Path

from app.ingestion.filesystem import SourceFile

IGNORED_DIRECTORIES = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    "dist",
    "build",
    "coverage",
}

IGNORED_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".ai",
    ".zip",
    ".exe",
    ".dll",
    ".key",
    ".pem",
}

SENSITIVE_FILES = {
    ".env",
}

MAX_FILE_SIZE_BYTES = 1 * 1024 * 1024  # 1 MB


@dataclass
class FilterResult:
    accepted: list[SourceFile] = field(default_factory=list)
    filtered: list[tuple[SourceFile, str]] = field(default_factory=list)


class FileFilter:
    def __init__(
        self,
        ignored_directories: set[str] = IGNORED_DIRECTORIES,
        ignored_extensions: set[str] = IGNORED_EXTENSIONS,
        sensitive_files: set[str] = SENSITIVE_FILES,
        max_file_size_bytes: int = MAX_FILE_SIZE_BYTES,
    ):
        self.ignored_directories = ignored_directories
        self.ignored_extensions = ignored_extensions
        self.sensitive_files = sensitive_files
        self.max_file_size_bytes = max_file_size_bytes

    def filter(self, files: list[SourceFile]) -> FilterResult:
        result = FilterResult()

        for file in files:
            path_parts = Path(file.relative_path).parts
            file_name = Path(file.relative_path).name
            extension = Path(file.relative_path).suffix.lower()

            # 1. Directory Check
            if any(part in self.ignored_directories for part in path_parts):
                result.filtered.append((file, "ignored_directory"))
                continue

            # 2. Extension Check
            if extension in self.ignored_extensions:
                result.filtered.append((file, "ignored_extension"))
                continue

            # 3. Sensitive File Check
            if file_name in self.sensitive_files:
                result.filtered.append((file, "sensitive_file"))
                continue

            # 4. File Size Check
            if file.size_bytes > self.max_file_size_bytes:
                result.filtered.append((file, "exceeds_size_limit"))
                continue

            result.accepted.append(file)

        return result
