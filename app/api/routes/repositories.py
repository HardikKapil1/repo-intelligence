# app/api/routes/repositories.py
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.repository import RepositoryCreate, RepositoryResponse
from app.services import repository_service
from app.services.ingestion_service import IngestionService

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


@router.post("/repositories/{repository_id}/index")
def index_repository(
    repository_id: UUID,
    db: Session = Depends(get_db),  # noqa: B008
):
    service = IngestionService(db)

    try:
        service.index_repository(repository_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc
    
    return {
        "repository_id": str(repository_id),
        "status": "indexing_completed",
    }
