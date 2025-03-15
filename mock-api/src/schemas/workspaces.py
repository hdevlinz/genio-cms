from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class WorkspaceViewModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class WorkspaceSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str


class CreateWorkspaceSchema(BaseModel):
    name: str


class UpdateWorkspaceSchema(BaseModel):
    name: Optional[str] = None
