from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.repository import RepositoryCreate, RepositoryResponse
from app.services import repository_service

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
