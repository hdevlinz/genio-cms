from fastapi import APIRouter

from src.api.news import news_router
from src.api.articles import article_router
from src.api.channels import channel_router
from src.api.videos import video_router
from src.api.workspaces import workspace_router

channel_prefix = "/workspaces/{workspace_id}"
article_video_prefix = "/workspaces/{workspace_id}/channels/{channel_id}"

main_router = APIRouter(prefix="/api/v1")
main_router.include_router(news_router)
main_router.include_router(workspace_router)
main_router.include_router(channel_router, prefix=channel_prefix)
main_router.include_router(article_router, prefix=article_video_prefix)
main_router.include_router(video_router, prefix=article_video_prefix)
