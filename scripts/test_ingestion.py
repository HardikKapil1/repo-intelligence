import sys
from pathlib import Path
from uuid import uuid4

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.ingestion.filesystem import FileDiscovery
from app.ingestion.filter import FileFilter
from app.ingestion.github import GitHubCloner
from app.ingestion.language import LanguageDetector


def main():
    base_storage_path = Path("data/repositories")
    target_url = "https://github.com/psf/requests"
    repo_id = uuid4()

    print(f"Cloning repository: {target_url}...")
    cloner = GitHubCloner(base_path=base_storage_path)
    repo_path = cloner.clone(repository_url=target_url, repository_id=repo_id)

    # 1. Discover all raw files
    discovery = FileDiscovery()
    raw_files = discovery.discover(repo_path)

    # 2. Filter files
    file_filter = FileFilter()
    filter_result = file_filter.filter(raw_files)

    # 3. Detect languages for accepted files
    detector = LanguageDetector()

    print(f"\nDiscovered: {len(raw_files)}")
    print(f"Accepted:   {len(filter_result.accepted)}")
    print(f"Filtered:   {len(filter_result.filtered)}\n")

    print(f"{'Accepted File':<55} | {'Detected Language':<20}")
    print("-" * 78)

    for file in filter_result.accepted:
        language = detector.detect(Path(file.relative_path))
        lang_str = language if language else "Unknown (None)"
        print(f"{file.relative_path:<55} | {lang_str:<20}")


if __name__ == "__main__":
    main()
