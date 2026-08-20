# scripts/run_index.py
from app.core.database import (
    SessionLocal,
)  # apna actual session factory path check kar lena
from app.models.repository import Repository
from app.services.ingestion_service import IngestionService


def main():
    db = SessionLocal()
    try:
        repo = db.query(Repository).first()  # ya specific ID daal do
        if repo is None:
            print("No repository found in DB")
            return
        print(f"Indexing: {repo.github_url}")
        service = IngestionService(db)
        service.index_repository(repo.id)
    finally:
        db.close()


if __name__ == "__main__":
    main()
