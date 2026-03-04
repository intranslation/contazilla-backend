from interface.deps.database import get_db
from fastapi import Depends
from typing import Annotated, Any

from infrastructure.repositories.asset import AssetRepository
from infrastructure.repositories.client import ClientRepository
from application.use_cases.asset import (
    CreateAsset,
    GetAsset,
    ListAssets,
    UpdateAsset,
    DeleteAsset,
    AssignClientToAsset,
)


def get_asset_repo(db: Annotated[Any, Depends(get_db)]) -> AssetRepository:
    return AssetRepository(db=db)


def create_asset_use_case(
    asset_repository: Annotated[AssetRepository, Depends(get_asset_repo)],
):
    return CreateAsset(asset_repo=asset_repository)


def get_asset_use_case(
    asset_repository: Annotated[AssetRepository, Depends(get_asset_repo)],
):
    return GetAsset(asset_repo=asset_repository)


def list_assets_use_case(
    asset_repository: Annotated[AssetRepository, Depends(get_asset_repo)],
):
    return ListAssets(asset_repo=asset_repository)


def update_asset_use_case(
    asset_repository: Annotated[AssetRepository, Depends(get_asset_repo)],
):
    return UpdateAsset(asset_repo=asset_repository)


def delete_asset_use_case(
    asset_repository: Annotated[AssetRepository, Depends(get_asset_repo)],
):
    return DeleteAsset(asset_repo=asset_repository)


def get_client_repo_for_asset(db: Annotated[Any, Depends(get_db)]) -> ClientRepository:
    return ClientRepository(db=db)


def assign_client_to_asset_use_case(
    asset_repository: Annotated[AssetRepository, Depends(get_asset_repo)],
    client_repository: Annotated[ClientRepository, Depends(get_client_repo_for_asset)],
):
    return AssignClientToAsset(asset_repo=asset_repository, client_repo=client_repository)
