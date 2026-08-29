# app/api/routes/repositories.py
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.repository import RepositoryCreate, RepositoryResponse
from app.services import repository_service
from app.workers.ingestion_worker import index_repository_job
from app.workers.queue import ingestion_queue

router = APIRouter()


@router.post(
    "/repositories",
    response_model=RepositoryResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_repository(
    repository_in: RepositoryCreate,
    db: Session = Depends(get_db),  # noqa: B008
):
    """
    Create a new repository entry via the service layer.
    """
    return repository_service.create_repository(db=db, repository_in=repository_in)


@router.post(
    "/repositories/{repository_id}/index",
    status_code=status.HTTP_202_ACCEPTED,
)
def index_repository(
    repository_id: UUID,
    db: Session = Depends(get_db),  # noqa: B008
):
    repository = repository_service.get_repository_by_id(
        db,
        repository_id,
    )

    if repository is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Repository not found",
        )

    job = ingestion_queue.enqueue(
        index_repository_job,
        str(repository_id),
    )

    return {
        "repository_id": str(repository_id),
        "job_id": job.id,
        "status": "queued",
    }
