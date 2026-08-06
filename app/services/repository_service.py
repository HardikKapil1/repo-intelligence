# app/services/repository_service.py
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.repository import Repository, RepositoryStatus
from app.schemas.repository import RepositoryCreate


def get_repository_by_id(db: Session, repo_id: UUID) -> Repository | None:
    return db.query(Repository).filter(Repository.id == repo_id).first()


def get_repository_by_url(db: Session, github_url: str) -> Repository | None:
    return db.query(Repository).filter(Repository.github_url == github_url).first()


def create_repository(db: Session, repository_in: RepositoryCreate) -> Repository:
    url_str = str(repository_in.github_url)

    # 1. Check duplicate URL
    existing_repo = get_repository_by_url(db, github_url=url_str)
    if existing_repo:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Repository already exists",
        )

    # 2. Create SQLAlchemy model with initial status = PENDING
    db_repo = Repository(
        github_url=url_str,
        status=RepositoryStatus.PENDING,
    )

    # 3. Commit & Refresh
    db.add(db_repo)
    db.commit()
    db.refresh(db_repo)

    return db_repo