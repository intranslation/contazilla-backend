import mimetypes
from collections.abc import Generator
from typing import Callable, TypedDict
from uuid import UUID

from application.ports.asset_repository import AssetRepository
from application.ports.bucket_handler import BucketHandler
from application.ports.client_repository import ClientRepository


class RetrieveAssetResponse(TypedDict):
    file: Callable[[], Generator[bytes, None, None]]
    filename: str
    media_type: str


class RetrieveAsset:
    def __init__(
        self,
        asset_repo: AssetRepository,
        client_repo: ClientRepository,
        bucket_handler: BucketHandler,
    ):
        self.asset_repo: AssetRepository = asset_repo
        self.client_repo: ClientRepository = client_repo
        self.bucket_handler: BucketHandler = bucket_handler

    def execute(
        self,
        client_id: UUID,
        asset_id: UUID,
        user_id: UUID,
    ) -> RetrieveAssetResponse:

        asset = self.asset_repo.get_by_id(asset_id=asset_id, user_id=user_id)

        if asset is None:
            raise ValueError("Asset with the id provided doesn't exists")

        key = f"{str(user_id)}/{str(client_id)}/{asset.filename}"

        obj = self.bucket_handler.retrieve_file(key=key)
        content_type = (
            obj.get("ContentType")
            or mimetypes.guess_type(key)[0]
            or "application/octet-stream"
        )
        body = obj["Body"]

        def iterfile():
            for chunk in iter(lambda: body.read(1024 * 1024), b""):
                yield chunk

        return {
            "file": iterfile,
            "filename": asset.filename,
            "media_type": content_type,
        }
