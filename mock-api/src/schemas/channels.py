from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from src.schemas.workspaces import WorkspaceSchema


class ChannelViewModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    workspace_id: UUID
    category: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ChannelSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    category: str
    workspace: WorkspaceSchema


class CreateChannelSchema(BaseModel):
    workspace_id: UUID
    category: str


class UpdateChannelSchema(BaseModel):
    workspace_id: Optional[UUID] = None
    category: Optional[str] = None
