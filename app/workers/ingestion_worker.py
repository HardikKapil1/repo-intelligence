from uuid import UUID

from app.core.database import SessionLocal
from app.services.ingestion_service import IngestionService


def index_repository_job(repository_id: str) -> None:
    db = SessionLocal()

    try:
        service = IngestionService(db)
        service.index_repository(UUID(repository_id))
    finally:
        db.close()
