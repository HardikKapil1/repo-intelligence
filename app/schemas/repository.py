# app/schemas/repository.py
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from app.models.enums import RepositoryStatus


class RepositoryCreate(BaseModel):
    github_url: HttpUrl = Field(..., description="GitHub repository URL")


class RepositoryResponse(BaseModel):
    id: UUID = Field(..., description="Unique identifier for the repository")
    github_url: HttpUrl = Field(..., description="GitHub repository URL")
    name: str | None = Field(None, max_length=100, description="Name of the repository")
    owner: str | None = Field(
        None, max_length=100, description="Owner of the repository"
    )
    default_branch: str | None = Field(
        None, max_length=50, description="Default branch of the repository"
    )
    commit_sha: str | None = Field(
        None, max_length=40, description="Latest commit SHA of the repository"
    )
    status: RepositoryStatus = Field(
        default=RepositoryStatus.PENDING,
        description="Status of the repository processing",
    )
    created_at: datetime = Field(
        ..., description="Timestamp when the repository was created"
    )
    updated_at: datetime = Field(
        ..., description="Timestamp when the repository was last updated"
    )

    model_config = ConfigDict(from_attributes=True)
