from typing import Any, Dict, List, Optional
from uuid import UUID

from faker import Faker
from fastapi import APIRouter, HTTPException, Query
from pydantic import TypeAdapter

from src import load_data_from_json
from src.schemas.articles import ArticleSchema, ArticleViewModel
from src.schemas.videos import VideoSchema, VideoViewModel

news_router = APIRouter(prefix="/news", tags=["News"])
fake = Faker()


@news_router.get("/articles", response_model=Dict[str, Any])
async def get_all_articles(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1),
    search: Optional[str] = Query(None),
) -> Dict[str, Any]:
    articles_data = load_data_from_json("articles.json")

    if search:
        articles_data = [
            art
            for art in articles_data
            if search.lower() in art["original_url"].lower()
            or search.lower() in art["content"].lower()
        ]

    start_index = (page - 1) * size
    end_index = start_index + size
    paginated_articles = articles_data[start_index:end_index]

    rs = TypeAdapter(List[ArticleViewModel]).validate_python(
        paginated_articles,
        from_attributes=True,
    )

    return {"data": {"items": rs, "total": len(articles_data)}}


@news_router.get("/articles/{article_id}", response_model=Dict[str, Any])
async def get_article(article_id: UUID) -> Dict[str, Any]:
    workspaces = load_data_from_json("workspaces.json")
    channels = load_data_from_json("channels.json")
    articles = load_data_from_json("articles.json")

    for article in articles:
        if article["id"] == str(article_id):
            channel = next(
                (ws for ws in channels if ws["id"] == article["channel_id"]), None
            )
            workspace = next(
                (ws for ws in workspaces if ws["id"] == channel["workspace_id"]), None
            )
            channel["workspace"] = workspace
            rs = TypeAdapter(ArticleSchema).validate_python(
                {**article, "channel": channel},
                from_attributes=True,
            )

            return {"data": rs}

    raise HTTPException(status_code=404, detail="Article not found")


@news_router.get("/videos", response_model=Dict[str, Any])
async def get_all_videos(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1),
    search: Optional[str] = Query(None),
) -> Dict[str, Any]:
    videos_data = load_data_from_json("videos.json")

    if search:
        videos_data = [
            vid
            for vid in videos_data
            if search.lower() in vid["result_video_url"].lower()
            or search.lower() in vid["audio_file"].lower()
            or any(
                search.lower() in segment.lower() for segment in vid["video_segments"]
            )
        ]

    start_index = (page - 1) * size
    end_index = start_index + size
    paginated_videos = videos_data[start_index:end_index]

    rs = TypeAdapter(List[VideoViewModel]).validate_python(
        paginated_videos,
        from_attributes=True,
    )

    return {"data": {"items": rs, "total": len(videos_data)}}


@news_router.get("/videos/{video_id}", response_model=Dict[str, Any])
async def get_video(video_id: UUID) -> Dict[str, Any]:
    workspaces = load_data_from_json("workspaces.json")
    channels = load_data_from_json("channels.json")
    articles = load_data_from_json("articles.json")
    videos = load_data_from_json("videos.json")

    for video in videos:
        if video["id"] == str(video_id):
            channel = next(
                (ws for ws in channels if ws["id"] == video["channel_id"]), None
            )
            workspace = next(
                (ws for ws in workspaces if ws["id"] == channel["workspace_id"]), None
            )
            channel["workspace"] = workspace
            articles_with_channels = []
            for article in articles:
                if article["id"] in video["article_ids"]:
                    article_channel = next(
                        (ch for ch in channels if ch["id"] == article["channel_id"]),
                        None,
                    )
                    if article_channel:
                        article_channel_workspace = next(
                            (
                                ws
                                for ws in workspaces
                                if ws["id"] == article_channel["workspace_id"]
                            ),
                            None,
                        )
                        article_channel["workspace"] = article_channel_workspace
                    articles_with_channels.append(
                        {**article, "channel": article_channel}
                    )

            articles = TypeAdapter(List[ArticleSchema]).validate_python(
                articles_with_channels,
                from_attributes=True,
            )
            rs = TypeAdapter(VideoSchema).validate_python(
                {**video, "channel": channel, "articles": articles},
                from_attributes=True,
            )

            return {"data": rs}

    raise HTTPException(status_code=404, detail="Video not found")
