from enum import Enum

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
    def classify(
        self,
        source_file: SourceFile,
    ) -> FileCategory:
        if source_file.language in CODE_LANGUAGES:
            return FileCategory.CODE

        if source_file.language in DOCUMENTATION_LANGUAGES:
            return FileCategory.DOCUMENTATION

        if source_file.language in CONFIGURATION_LANGUAGES:
            return FileCategory.CONFIGURATION

        return FileCategory.UNKNOWN
