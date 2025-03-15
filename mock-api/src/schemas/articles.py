from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from src.schemas.channels import ChannelSchema


class ArticleViewModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    channel_id: UUID
    title: str
    content: str
    original_url: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ArticleSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    channel: ChannelSchema
    title: str
    content: str
    original_url: str
    related_urls: List[str] = []
    images: List[str] = []


class CreateArticleSchema(BaseModel):
    channel_id: UUID
    title: str
    content: str
    original_url: str
    related_urls: List[str] = []
    images: List[str] = []


class UpdateArticleSchema(BaseModel):
    channel_id: Optional[UUID] = None
    title: Optional[str] = None
    content: Optional[str] = None
    original_url: Optional[str] = None
    related_urls: Optional[List[str]] = None
    images: Optional[List[str]] = None
