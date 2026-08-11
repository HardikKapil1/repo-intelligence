from pathlib import Path

# Mapping file extensions to language identifiers
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

# Mapping exact filenames (case-insensitive) to language identifiers
EXACT_FILENAME_MAP: dict[str, str] = {
    "dockerfile": "dockerfile",
    "makefile": "makefile",
}


class LanguageDetector:
    def detect(self, path: Path | str) -> str | None:
        file_path = Path(path)
        file_name = file_path.name.lower()

        # 1. Check exact special filenames first
        if file_name in EXACT_FILENAME_MAP:
            return EXACT_FILENAME_MAP[file_name]

        # 2. Check extension mapping
        extension = file_path.suffix.lower()
        if extension in EXTENSION_MAP:
            return EXTENSION_MAP[extension]

        # 3. Unknown or unmapped language
        return None
