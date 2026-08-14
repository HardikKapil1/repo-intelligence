from enum import Enum
from pathlib import Path

from app.ingestion.filesystem import SourceFile


class FileCategory(str, Enum):
    CODE = "code"
    DOCUMENTATION = "documentation"
    CONFIGURATION = "configuration"
    UNKNOWN = "unknown"


CODE_LANGUAGES = {
    "python",
    "javascript",
    "typescript",
    "java",
    "go",
    "rust",
    "cpp",
    "c",
    "ruby",
    "php",
}

DOCUMENTATION_LANGUAGES = {
    "markdown",
    "rst",
}

CONFIGURATION_LANGUAGES = {
    "yaml",
    "json",
    "toml",
    "css",
    "html",
    "makefile",
    "dockerfile",
}


class FileClassifier:
    def classify(self, source_file: SourceFile) -> FileCategory:
        if source_file.language in CODE_LANGUAGES:
            return FileCategory.CODE

        if source_file.language in DOCUMENTATION_LANGUAGES:
            return FileCategory.DOCUMENTATION

        if source_file.language in CONFIGURATION_LANGUAGES:
            return FileCategory.CONFIGURATION

        return FileCategory.UNKNOWN

    def _detect_language(self, source_file: SourceFile) -> str | None:
        path = Path(source_file.path)

        # Special filenames
        special_files = {
            "Dockerfile": "dockerfile",
            "Makefile": "makefile",
        }

        if path.name in special_files:
            return special_files[path.name]

        return self._language_from_extension(path.suffix.lower())

    def _language_from_extension(self, extension: str) -> str | None:
        languages = {
            ".py": "python",
            ".js": "javascript",
            ".jsx": "javascript",
            ".ts": "typescript",
            ".tsx": "typescript",
            ".java": "java",
            ".go": "go",
            ".rs": "rust",
            ".cpp": "cpp",
            ".cc": "cpp",
            ".c": "c",
            ".h": "c",
            ".hpp": "cpp",
            ".rb": "ruby",
            ".php": "php",
            ".md": "markdown",
            ".rst": "rst",
            ".yml": "yaml",
            ".yaml": "yaml",
            ".json": "json",
            ".toml": "toml",
            ".css": "css",
            ".html": "html",
        }

        return languages.get(extension)
