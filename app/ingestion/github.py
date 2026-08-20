# app/ingestion/github.py
import subprocess
from pathlib import Path
from uuid import UUID

from app.ingestion.exceptions import RepositoryCloneError


class GitHubCloner:
    def __init__(self, base_path: Path) -> None:
        self.base_path = base_path

    def clone(self, repository_url: str, repository_id: UUID) -> Path:
        destination = self.base_path / str(repository_id)

        if destination.exists():
            raise RepositoryCloneError(
                f"Repository destination already exists: {destination}"
            )

        self.base_path.mkdir(parents=True, exist_ok=True)

        try:
            subprocess.run(
                [
                    "git",
                    "clone",
                    "--depth",
                    "1",
                    repository_url,
                    str(destination),
                ],
                check=True,
                capture_output=True,
                text=True,
                timeout=300,
            )
        except subprocess.TimeoutExpired as exc:
            raise RepositoryCloneError(
                "Repository clone timed out after 5 minutes."
            ) from exc
        except subprocess.CalledProcessError as exc:
            error = exc.stderr.strip() or "Unknown git error."
            raise RepositoryCloneError(f"Failed to clone repository: {error}") from exc
        except OSError as exc:
            raise RepositoryCloneError(
                "Git is not installed or could not be executed."
            ) from exc

        return destination
