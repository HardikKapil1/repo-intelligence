from pathlib import Path

from app.ingestion.classification import FileClassifier
from app.ingestion.filesystem import FileDiscovery, SourceFile
from app.ingestion.language import LanguageDetector


def main():
    repos_dir = Path("data/repositories")

    # Find the first directory inside data/repositories
    repo_folders = [d for d in repos_dir.iterdir() if d.is_dir()]

    if not repo_folders:
        print("❌ No repository folders found in data/repositories/")
        return

    repo_path = repo_folders[0]
    print(f"📁 Testing ingestion on repository: {repo_path.name}\n")

    # 1. Discover raw files
    discovery = FileDiscovery()
    raw_files = discovery.discover(repo_path)

    # 2. Language Detection & Classification
    detector = LanguageDetector()
    classifier = FileClassifier()

    classified_files: list[tuple[SourceFile, str]] = []

    for raw_file in raw_files:
        lang = detector.detect(raw_file.path)

        source_file = SourceFile(
            path=raw_file.path,
            relative_path=raw_file.relative_path,
            size_bytes=raw_file.size_bytes,
            language=lang,
        )

        category = classifier.classify(source_file)
        classified_files.append((source_file, category.value))

    # 3. Print output in table format
    print(f"{'Path':<45} {'Language':<14} {'Category':<15}")
    print("-" * 74)

    for file, category in classified_files:
        lang_str = file.language if file.language else "unknown"
        print(f"{file.relative_path:<45} {lang_str:<14} {category:<15}")


if __name__ == "__main__":
    main()
