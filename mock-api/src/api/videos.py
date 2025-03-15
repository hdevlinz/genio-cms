from typing import Any, Dict, List, Optional
from uuid import UUID

from faker import Faker
from fastapi import APIRouter, Body, HTTPException, Query, Response
from fastapi.responses import JSONResponse
from pydantic import TypeAdapter

from src import load_data_from_json, save_data_to_json
from src.schemas.articles import ArticleSchema
from src.schemas.videos import VideoSchema, VideoViewModel

video_router = APIRouter(prefix="/videos", tags=["Videos"])
fake = Faker()


@video_router.get("", response_model=Dict[str, Any])
async def get_videos(
    workspace_id: UUID,
    channel_id: UUID,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1),
    search: Optional[str] = Query(None),
) -> Dict[str, Any]:
    videos_data = load_data_from_json("videos.json")
    videos_data = [vid for vid in videos_data if vid["channel_id"] == str(channel_id)]

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


@video_router.get("/{video_id}", response_model=Dict[str, Any])
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


@video_router.post("", response_model=Dict[str, Any], status_code=201)
async def create_video(
    workspace_id: UUID,
    channel_id: UUID,
    video: Dict[str, Any] = Body(...),
) -> Dict[str, Any]:
    workspaces = load_data_from_json("workspaces.json")
    channels = load_data_from_json("channels.json")
    articles = load_data_from_json("articles.json")
    videos = load_data_from_json("videos.json")

    video["id"] = fake.uuid4()
    video["channel_id"] = channel_id
    video["workspace_id"] = workspace_id
    videos.append(video)
    save_data_to_json("videos.json", videos)

    channel = next((ws for ws in channels if ws["id"] == video["channel_id"]), None)
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
                workspace = next(
                    (
                        ws
                        for ws in workspaces
                        if ws["id"] == article_channel["workspace_id"]
                    ),
                    None,
                )
                article_channel["workspace"] = workspace
            articles_with_channels.append({**article, "channel": article_channel})

    articles = TypeAdapter(List[Dict[str, Any]]).validate_python(
        articles_with_channels,
        from_attributes=True,
    )
    rs = TypeAdapter(VideoSchema).validate_python(
        {**video, "channel": channel, "articles": articles},
        from_attributes=True,
    )

    return {"data": rs}


@video_router.put("/{video_id}", response_model=Dict[str, Any])
async def update_video(
    workspace_id: UUID,
    channel_id: UUID,
    video_id: UUID,
    updated_video: Dict[str, Any] = Body(...),
) -> Dict[str, Any]:
    workspaces = load_data_from_json("workspaces.json")
    channels = load_data_from_json("channels.json")
    articles = load_data_from_json("articles.json")
    videos = load_data_from_json("videos.json")

    for index, video in enumerate(videos):
        if video["id"] == str(video_id):
            updated_video["id"] = video_id
            updated_video["channel_id"] = channel_id
            updated_video["workspace_id"] = workspace_id
            videos[index] = updated_video
            save_data_to_json("videos.json", videos)

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
                        workspace = next(
                            (
                                ws
                                for ws in workspaces
                                if ws["id"] == article_channel["workspace_id"]
                            ),
                            None,
                        )
                        article_channel["workspace"] = workspace
                    articles_with_channels.append(
                        {**article, "channel": article_channel}
                    )

            articles = TypeAdapter(List[Dict[str, Any]]).validate_python(
                articles_with_channels,
                from_attributes=True,
            )
            rs = TypeAdapter(VideoSchema).validate_python(
                {**updated_video, "channel": channel, "articles": articles},
                from_attributes=True,
            )

            return {"data": rs}

    raise HTTPException(status_code=404, detail="Video not found")


@video_router.delete("/{video_id}", status_code=204)
async def delete_video(
    workspace_id: UUID,
    channel_id: UUID,
    video_id: UUID,
) -> Response:
    videos = load_data_from_json("videos.json")
    updated_videos = [vid for vid in videos if vid["id"] != str(video_id)]

    if len(updated_videos) < len(videos):
        save_data_to_json("videos.json", updated_videos)
        return JSONResponse(status_code=204, content=None)

    raise HTTPException(status_code=404, detail="Video not found")
