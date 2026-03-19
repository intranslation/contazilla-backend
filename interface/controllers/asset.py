import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import StreamingResponse

from application.use_cases.asset import (AssignClientToAsset, DeleteAsset,
                                         GetAsset, ListAssets, UpdateAsset)
from application.use_cases.asset.retrieve_asset import RetrieveAsset
from application.use_cases.asset.upload_asset import UploadAsset
from domain.entities.user import User
from interface.deps import (assign_client_to_asset_use_case,
                            delete_asset_use_case, get_asset_use_case,
                            get_current_user_use_case, list_assets_use_case,
                            update_asset_use_case)
from interface.deps.asset import retrieve_asset_use_case, upload_asset_use_case
from interface.schemas import AssetResponse, AssetUpdate, AssignClient

router = APIRouter(prefix="/assets", tags=["assets"])


@router.get("/", response_model=list[AssetResponse])
def list_all(
    current_user: Annotated[User, Depends(get_current_user_use_case)],
    use_case: Annotated[ListAssets, Depends(list_assets_use_case)],
    client_id: UUID | None = None,
):
    assets = use_case.execute(user_id=current_user.id, client_id=client_id)
    return [
        AssetResponse(
            id=str(a.id),
            filename=a.filename,
            client_id=str(a.client_id) if a.client_id else None,
            user_id=str(a.user_id),
            size=a.size,
            was_viewed=a.was_viewed,
            was_downloaded=a.was_downloaded,
            created_at=a.created_at,
            updated_at=a.updated_at,
        )
        for a in assets
    ]


@router.post("/retrieve", status_code=status.HTTP_201_CREATED)
def retrieve_asset(
    asset_id: str,
    client_id: str,
    current_user: Annotated[User, Depends(get_current_user_use_case)],
    use_case: Annotated[RetrieveAsset, Depends(retrieve_asset_use_case)],
):
    response = use_case.execute(
        asset_id=UUID(asset_id), client_id=UUID(client_id), user_id=current_user.id
    )

    headers = {"Content-Disposition": f'attachment; filename="{response['filename']}"'}

    return StreamingResponse(
        content=response["file"](), media_type=response["media_type"], headers=headers
    )


@router.get("/{asset_id}", response_model=AssetResponse)
def get_by_id(
    asset_id: UUID,
    current_user: Annotated[User, Depends(get_current_user_use_case)],
    use_case: Annotated[GetAsset, Depends(get_asset_use_case)],
):
    try:
        asset = use_case.execute(asset_id=asset_id, user_id=current_user.id)
        return AssetResponse(
            id=str(asset.id),
            filename=asset.filename,
            client_id=str(asset.client_id) if asset.client_id else None,
            user_id=str(asset.user_id),
            size=asset.size,
            was_viewed=asset.was_viewed,
            was_downloaded=asset.was_downloaded,
            created_at=asset.created_at,
            updated_at=asset.updated_at,
        )
    except ValueError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e))


@router.put("/{asset_id}", response_model=AssetResponse)
def update(
    asset_id: UUID,
    data: AssetUpdate,
    current_user: Annotated[User, Depends(get_current_user_use_case)],
    use_case: Annotated[UpdateAsset, Depends(update_asset_use_case)],
):
    try:
        asset = use_case.execute(
            asset_id=asset_id,
            user_id=current_user.id,
            filename=data.filename,
            client_id=UUID(data.client_id) if data.client_id else None,
            was_viewed=data.was_viewed,
            was_downloaded=data.was_downloaded,
        )
        return AssetResponse(
            id=str(asset.id),
            filename=asset.filename,
            client_id=str(asset.client_id) if asset.client_id else None,
            user_id=str(asset.user_id),
            size=asset.size,
            was_viewed=asset.was_viewed,
            was_downloaded=asset.was_downloaded,
            created_at=asset.created_at,
            updated_at=asset.updated_at,
        )
    except ValueError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e))


@router.delete("/{asset_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    asset_id: UUID,
    current_user: Annotated[User, Depends(get_current_user_use_case)],
    use_case: Annotated[DeleteAsset, Depends(delete_asset_use_case)],
):
    try:
        use_case.execute(asset_id=asset_id, user_id=current_user.id)
    except ValueError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e))


@router.patch("/{asset_id}/client", response_model=AssetResponse)
def assign_client(
    asset_id: UUID,
    data: AssignClient,
    current_user: Annotated[User, Depends(get_current_user_use_case)],
    use_case: Annotated[AssignClientToAsset, Depends(assign_client_to_asset_use_case)],
):
    try:
        asset = use_case.execute(
            asset_id=asset_id,
            user_id=current_user.id,
            client_id=UUID(data.client_id) if data.client_id else None,
        )
        return AssetResponse(
            id=str(asset.id),
            filename=asset.filename,
            client_id=str(asset.client_id) if asset.client_id else None,
            user_id=str(asset.user_id),
            size=asset.size,
            was_viewed=asset.was_viewed,
            was_downloaded=asset.was_downloaded,
            created_at=asset.created_at,
            updated_at=asset.updated_at,
        )
    except ValueError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e))


@router.post("/upload", status_code=status.HTTP_201_CREATED)
def upload_asset(
    client_id: str,
    file: UploadFile,
    current_user: Annotated[User, Depends(get_current_user_use_case)],
    use_case: Annotated[UploadAsset, Depends(upload_asset_use_case)],
):
    filename: str = file.filename if file.filename else f"{datetime.UTC}"
    return use_case.execute(
        file=file.file,
        filename=filename,
        client_id=UUID(client_id),
        user_id=current_user.id,
    )
