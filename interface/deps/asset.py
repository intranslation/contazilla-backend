from typing import Annotated, Any

from fastapi import Depends

from application.use_cases.asset import (AssignClientToAsset, DeleteAsset,
                                         GetAsset, ListAssets, UpdateAsset)
from application.use_cases.asset.retrieve_asset import RetrieveAsset
from application.use_cases.asset.upload_asset import UploadAsset
from infrastructure.repositories.asset import AssetRepository
from infrastructure.repositories.client import ClientRepository
from infrastructure.services.bucket_handler import BucketHandler
from interface.deps.database import get_db
from interface.deps.externals import get_bucket_handler


def get_asset_repo(db: Annotated[Any, Depends(get_db)]) -> AssetRepository:
    return AssetRepository(db=db)


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
    return AssignClientToAsset(
        asset_repo=asset_repository, client_repo=client_repository
    )


def upload_asset_use_case(
    asset_repository: Annotated[AssetRepository, Depends(get_asset_repo)],
    client_repository: Annotated[ClientRepository, Depends(get_client_repo_for_asset)],
    bucket_handler: Annotated[BucketHandler, Depends(get_bucket_handler)],
):
    return UploadAsset(
        asset_repo=asset_repository,
        client_repo=client_repository,
        bucket_handler=bucket_handler,
    )


def retrieve_asset_use_case(
    asset_repository: Annotated[AssetRepository, Depends(get_asset_repo)],
    client_repository: Annotated[ClientRepository, Depends(get_client_repo_for_asset)],
    bucket_handler: Annotated[BucketHandler, Depends(get_bucket_handler)],
):
    return RetrieveAsset(
        asset_repo=asset_repository,
        client_repo=client_repository,
        bucket_handler=bucket_handler,
    )
