from typing import Any, Dict, List, Optional
from uuid import UUID

from faker import Faker
from fastapi import APIRouter, Body, HTTPException, Query, Response
from fastapi.responses import JSONResponse
from pydantic import TypeAdapter

from src import load_data_from_json, save_data_to_json
from src.schemas.articles import ArticleSchema, ArticleViewModel

article_router = APIRouter(prefix="/articles", tags=["Articles"])
fake = Faker()


@article_router.get("", response_model=Dict[str, Any])
async def get_articles(
    workspace_id: UUID,
    channel_id: UUID,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1),
    search: Optional[str] = Query(None),
) -> Dict[str, Any]:
    articles_data = load_data_from_json("articles.json")
    articles_data = [
        art for art in articles_data if art["channel_id"] == str(channel_id)
    ]

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


@article_router.get("/{article_id}", response_model=Dict[str, Any])
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


@article_router.post("", response_model=Dict[str, Any], status_code=201)
async def create_article(
    workspace_id: UUID,
    channel_id: UUID,
    article: Dict[str, Any] = Body(...),
) -> Dict[str, Any]:
    workspaces = load_data_from_json("workspaces.json")
    channels = load_data_from_json("channels.json")
    articles = load_data_from_json("articles.json")

    article["id"] = fake.uuid4()
    article["channel_id"] = channel_id
    articles.append(article)
    save_data_to_json("articles.json", articles)

    channel = next((ws for ws in channels if ws["id"] == article["channel_id"]), None)
    workspace = next(
        (ws for ws in workspaces if ws["id"] == channel["workspace_id"]), None
    )
    channel["workspace"] = workspace
    rs = TypeAdapter(ArticleSchema).validate_python(
        {**article, "channel": channel},
        from_attributes=True,
    )
    return {"data": rs}


@article_router.put("/{article_id}", response_model=Dict[str, Any])
async def update_article(
    workspace_id: UUID,
    channel_id: UUID,
    article_id: UUID,
    updated_article: Dict[str, Any] = Body(...),
) -> Dict[str, Any]:
    workspaces = load_data_from_json("workspaces.json")
    channels = load_data_from_json("channels.json")
    articles = load_data_from_json("articles.json")

    for index, article in enumerate(articles):
        if article["id"] == str(article_id):
            updated_article["id"] = article_id
            updated_article["channel_id"] = channel_id
            updated_article["workspace_id"] = workspace_id
            articles[index] = updated_article
            save_data_to_json("articles.json", articles)

            channel = next(
                (ws for ws in channels if ws["id"] == article["channel_id"]), None
            )
            workspace = next(
                (ws for ws in workspaces if ws["id"] == channel["workspace_id"]), None
            )
            channel["workspace"] = workspace
            rs = TypeAdapter(ArticleSchema).validate_python(
                {**updated_article, "channel": channel},
                from_attributes=True,
            )
            return {"data": rs}

    raise HTTPException(status_code=404, detail="Article not found")


@article_router.delete("/{article_id}", status_code=204)
async def delete_article(
    workspace_id: UUID,
    channel_id: UUID,
    article_id: UUID,
) -> Response:
    articles = load_data_from_json("articles.json")
    updated_articles = [art for art in articles if art["id"] != str(article_id)]

    if len(updated_articles) < len(articles):
        save_data_to_json("articles.json", updated_articles)
        return JSONResponse(status_code=204, content=None)

    raise HTTPException(status_code=404, detail="Article not found")
