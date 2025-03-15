from typing import Any, Dict, List, Optional
from uuid import UUID

from faker import Faker
from fastapi import APIRouter, Body, HTTPException, Query, Response
from fastapi.responses import JSONResponse
from pydantic import TypeAdapter

from src import load_data_from_json, save_data_to_json
from src.schemas.channels import ChannelSchema, ChannelViewModel

channel_router = APIRouter(prefix="/channels", tags=["Channels"])
fake = Faker()


@channel_router.get("", response_model=Dict[str, Any])
async def get_channels(
    workspace_id: UUID,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1),
    search: Optional[str] = Query(None),
) -> Dict[str, Any]:
    channels_data = load_data_from_json("channels.json")
    channels_data = [
        ch for ch in channels_data if ch["workspace_id"] == str(workspace_id)
    ]

    if search:
        channels_data = [
            ch for ch in channels_data if search.lower() in ch["category"].lower()
        ]

    start_index = (page - 1) * size
    end_index = start_index + size
    paginated_channels = channels_data[start_index:end_index]

    rs = TypeAdapter(List[ChannelViewModel]).validate_python(
        paginated_channels,
        from_attributes=True,
    )

    return {"data": {"items": rs, "total": len(rs)}}


@channel_router.get("/{channel_id}", response_model=Dict[str, Any])
async def get_channel(channel_id: UUID) -> Dict[str, Any]:
    workspaces = load_data_from_json("workspaces.json")
    channels = load_data_from_json("channels.json")

    for channel in channels:
        if channel["id"] == str(channel_id):
            workspace = next(
                (ws for ws in workspaces if ws["id"] == channel["workspace_id"]), None
            )
            rs = TypeAdapter(ChannelSchema).validate_python(
                {**channel, "workspace": workspace},
                from_attributes=True,
            )

            return {"data": rs}

    raise HTTPException(status_code=404, detail="Channel not found")


@channel_router.post("", response_model=Dict[str, Any], status_code=201)
async def create_channel(
    workspace_id: UUID,
    channel: Dict[str, Any] = Body(...),
) -> Dict[str, Any]:
    workspaces = load_data_from_json("workspaces.json")
    channels = load_data_from_json("channels.json")

    channel["id"] = fake.uuid4()
    channel["workspace_id"] = workspace_id
    channels.append(channel)
    save_data_to_json("channels.json", channels)

    workspace = next(
        (ws for ws in workspaces if ws["id"] == channel["workspace_id"]), None
    )
    rs = TypeAdapter(ChannelSchema).validate_python(
        {**channel, "workspace": workspace},
        from_attributes=True,
    )
    return {"data": rs}


@channel_router.put("/{channel_id}", response_model=Dict[str, Any])
async def update_channel(
    workspace_id: UUID,
    channel_id: UUID,
    updated_channel: Dict[str, Any] = Body(...),
) -> Dict[str, Any]:
    workspaces = load_data_from_json("workspaces.json")
    channels = load_data_from_json("channels.json")

    for index, channel in enumerate(channels):
        if channel["id"] == str(channel_id):
            updated_channel["id"] = channel_id
            updated_channel["workspace_id"] = workspace_id
            channels[index] = updated_channel
            save_data_to_json("channels.json", channels)

            workspace = next(
                (ws for ws in workspaces if ws["id"] == channel["workspace_id"]), None
            )
            rs = TypeAdapter(ChannelSchema).validate_python(
                {**updated_channel, "workspace": workspace},
                from_attributes=True,
            )
            return {"data": rs}

    raise HTTPException(status_code=404, detail="Channel not found")


@channel_router.delete("/{channel_id}", status_code=204)
async def delete_channel(workspace_id: UUID, channel_id: UUID) -> Response:
    channels = load_data_from_json("channels.json")
    updated_channels = [ch for ch in channels if ch["id"] != str(channel_id)]

    if len(updated_channels) < len(channels):
        save_data_to_json("channels.json", updated_channels)
        return JSONResponse(status_code=204, content=None)

    raise HTTPException(status_code=404, detail="Channel not found")
