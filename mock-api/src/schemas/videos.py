from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from src.schemas.articles import ArticleSchema
from src.schemas.channels import ChannelSchema
from src.schemas.enums import VideoStatus


class VideoViewModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    channel_id: UUID
    article_ids: List[UUID] = []
    title: Optional[str] = None
    description: Optional[str] = None
    status: VideoStatus
    result_video_url: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class VideoSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    channel: ChannelSchema
    articles: List[ArticleSchema] = []
    title: Optional[str] = None
    description: Optional[str] = None
    status: VideoStatus
    result_video_url: Optional[str] = None
    audio_file: Optional[str] = None
    video_segments: Optional[List[str]] = None
    related_urls: Optional[List[str]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class CreateVideoSchema(BaseModel):
    channel_id: UUID
    article_ids: List[str] = []
    title: Optional[str] = None
    description: Optional[str] = None
    status: VideoStatus = VideoStatus.DRAFT


class UpdateVideoSchema(BaseModel):
    channel_id: Optional[UUID] = None
    article_ids: Optional[List[UUID]] = None
    title: Optional[str] = None
    description: Optional[str] = None
    status: VideoStatus = VideoStatus.DRAFT
