from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from application.use_cases.asset import (
    CreateAsset,
    GetAsset,
    ListAssets,
    UpdateAsset,
    DeleteAsset,
    AssignClientToAsset,
)
from domain.entities.user import User
from interface.deps import (
    get_current_user_use_case,
    create_asset_use_case,
    get_asset_use_case,
    list_assets_use_case,
    update_asset_use_case,
    delete_asset_use_case,
    assign_client_to_asset_use_case,
)
from interface.schemas import AssetCreate, AssetUpdate, AssetResponse, AssignClient

router = APIRouter(prefix="/assets", tags=["assets"])


@router.post("/", response_model=AssetResponse, status_code=status.HTTP_201_CREATED)
def create(
    data: AssetCreate,
    current_user: Annotated[User, Depends(get_current_user_use_case)],
    use_case: Annotated[CreateAsset, Depends(create_asset_use_case)],
):
    try:
        asset = use_case.execute(
            filename=data.filename,
            url=data.url,
            client_id=UUID(data.client_id) if data.client_id else None,
            user_id=current_user.id,
        )
        return AssetResponse(
            id=str(asset.id),
            filename=asset.filename,
            url=asset.url,
            client_id=str(asset.client_id) if asset.client_id else None,
            user_id=str(asset.user_id),
        )
    except ValueError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e))


@router.get("/", response_model=list[AssetResponse])
def list_all(
    current_user: Annotated[User, Depends(get_current_user_use_case)],
    use_case: Annotated[ListAssets, Depends(list_assets_use_case)],
):
    assets = use_case.execute(user_id=current_user.id)
    return [
        AssetResponse(
            id=str(a.id),
            filename=a.filename,
            url=a.url,
            client_id=str(a.client_id) if a.client_id else None,
            user_id=str(a.user_id),
        )
        for a in assets
    ]


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
            url=asset.url,
            client_id=str(asset.client_id) if asset.client_id else None,
            user_id=str(asset.user_id),
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
            url=data.url,
            client_id=UUID(data.client_id) if data.client_id else None,
        )
        return AssetResponse(
            id=str(asset.id),
            filename=asset.filename,
            url=asset.url,
            client_id=str(asset.client_id) if asset.client_id else None,
            user_id=str(asset.user_id),
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
            url=asset.url,
            client_id=str(asset.client_id) if asset.client_id else None,
            user_id=str(asset.user_id),
        )
    except ValueError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e))
