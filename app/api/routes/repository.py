# app/api/routes/repository.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.repository import RepositoryResponse

router = APIRouter()


@router.post("/repositories/", response_model=RepositoryResponse)
async def create_repository(
    repository: RepositoryResponse,
    db: Session = Depends(get_db),  # noqa
):
    """
    Create a new repository entry in the database.
    """
    db.add(repository)
    db.commit()
    db.refresh(repository)
    return repository
