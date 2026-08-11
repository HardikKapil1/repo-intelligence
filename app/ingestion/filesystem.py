from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SourceFile:
    path: Path
    relative_path: str
    size_bytes: int


class FileDiscovery:
    def discover(self, repository_path: Path) -> list[SourceFile]:
        if not repository_path.exists():
            raise FileNotFoundError(
                f"Repository path does not exist: {repository_path}"
            )
        if not repository_path.is_dir():
            raise NotADirectoryError(
                f"Repository path is not a directory: {repository_path}"
            )

        source_files: list[SourceFile] = []
        for path in repository_path.rglob("*"):
            if not path.is_file():
                continue

            relative_path = path.relative_to(repository_path)
            source_files.append(
                SourceFile(
                    path=path,
                    relative_path=relative_path.as_posix(),
                    size_bytes=path.stat().st_size,
                )
            )

        return source_files
