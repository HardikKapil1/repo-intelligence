# app/models/repository.py
import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base
from app.models.enums import RepositoryStatus


class Repository(Base):
    __tablename__ = "repositories"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    github_url: Mapped[str] = mapped_column(
        String(512),
        unique=True,
        index=True,
        nullable=False,
    )
    name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    owner: Mapped[str | None] = mapped_column(String(100), nullable=True)
    default_branch: Mapped[str | None] = mapped_column(String(50), nullable=True)
    commit_sha: Mapped[str | None] = mapped_column(String(40), nullable=True)

    status: Mapped[RepositoryStatus] = mapped_column(
        SQLEnum(RepositoryStatus, name="repository_status_enum"),
        default=RepositoryStatus.PENDING,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        server_onupdate=func.now(),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<Repository(id={self.id}, url='{self.github_url}', status='{self.status.value}')>"
