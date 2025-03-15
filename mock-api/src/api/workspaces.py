from typing import Any, Dict, List, Optional
from uuid import UUID

from fastapi import APIRouter, Body, HTTPException, Query, Response
from fastapi.responses import JSONResponse
from pydantic import TypeAdapter

from src import load_data_from_json, save_data_to_json
from faker import Faker
from src.schemas.workspaces import WorkspaceViewModel

workspace_router = APIRouter(prefix="/workspaces", tags=["Workspaces"])
fake = Faker()


@workspace_router.get("", response_model=Dict[str, Any])
async def get_workspaces(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1),
    search: Optional[str] = Query(None),
) -> Dict[str, Any]:
    workspaces_data = load_data_from_json("workspaces.json")

    if search:
        workspaces_data = [
            ws for ws in workspaces_data if search.lower() in ws["name"].lower()
        ]

    start_index = (page - 1) * size
    end_index = start_index + size
    paginated_workspaces = workspaces_data[start_index:end_index]

    rs = TypeAdapter(List[WorkspaceViewModel]).validate_python(
        paginated_workspaces,
        from_attributes=True,
    )

    return {"data": {"items": rs, "total": len(rs)}}


@workspace_router.get("/{workspace_id}", response_model=Dict[str, Any])
async def get_workspace(workspace_id: UUID) -> Dict[str, Any]:
    workspaces = load_data_from_json("workspaces.json")

    for workspace in workspaces:
        if workspace["id"] == str(workspace_id):
            rs = TypeAdapter(WorkspaceViewModel).validate_python(
                workspace,
                from_attributes=True,
            )

            return {"data": rs}

    raise HTTPException(status_code=404, detail="Workspace not found")


@workspace_router.post("", response_model=Dict[str, Any], status_code=201)
async def create_workspace(workspace: Dict[str, Any] = Body(...)) -> Dict[str, Any]:
    workspaces = load_data_from_json("workspaces.json")
    workspace["id"] = fake.uuid4()
    workspaces.append(workspace)
    save_data_to_json("workspaces.json", workspaces)

    rs = TypeAdapter(WorkspaceViewModel).validate_python(
        workspace,
        from_attributes=True,
    )
    return {"data": rs}


@workspace_router.put("/{workspace_id}", response_model=Dict[str, Any])
async def update_workspace(
    workspace_id: UUID,
    updated_workspace: Dict[str, Any] = Body(...),
) -> Dict[str, Any]:
    workspaces = load_data_from_json("workspaces.json")

    for index, workspace in enumerate(workspaces):
        if workspace["id"] == str(workspace_id):
            updated_workspace["id"] = workspace_id
            workspaces[index] = updated_workspace
            save_data_to_json("workspaces.json", workspaces)

            rs = TypeAdapter(WorkspaceViewModel).validate_python(
                updated_workspace,
                from_attributes=True,
            )
            return {"data": rs}

    raise HTTPException(status_code=404, detail="Workspace not found")


@workspace_router.delete("/{workspace_id}", status_code=204)
async def delete_workspace(workspace_id: UUID) -> Response:
    workspaces = load_data_from_json("workspaces.json")
    updated_workspaces = [
        workspace for workspace in workspaces if workspace["id"] != str(workspace_id)
    ]

    if len(updated_workspaces) < len(workspaces):
        save_data_to_json("workspaces.json", updated_workspaces)
        return JSONResponse(status_code=204, content=None)

    raise HTTPException(status_code=404, detail="Workspace not found")
