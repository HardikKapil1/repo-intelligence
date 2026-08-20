# app/ingestion/language.py
from pathlib import Path

EXTENSION_MAP: dict[str, str] = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".java": "java",
    ".go": "go",
    ".rs": "rust",
    ".cpp": "cpp",
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


EXACT_FILENAME_MAP: dict[str, str] = {
    "dockerfile": "dockerfile",
    "makefile": "makefile",
}


class LanguageDetector:
    def detect(
        self,
        path: Path | str,
    ) -> str | None:
        file_path = Path(path)

        file_name = file_path.name.lower()

        # Exact filenames first.
        if file_name in EXACT_FILENAME_MAP:
            return EXACT_FILENAME_MAP[file_name]

        # Then extensions.
        extension = file_path.suffix.lower()

        if extension in EXTENSION_MAP:
            return EXTENSION_MAP[extension]

        # Unknown file type.
        return None
