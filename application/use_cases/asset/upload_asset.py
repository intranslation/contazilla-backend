from typing import BinaryIO
from uuid import UUID

from application.ports.asset_repository import AssetRepository
from application.ports.bucket_handler import BucketHandler
from application.ports.client_repository import ClientRepository
from domain.entities.asset import Asset
from shared.config import settings


class UploadAsset:
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
        file: BinaryIO,
        filename: str,
        client_id: UUID,
        user_id: UUID,
    ):
        try:
            file.seek(0, 2)
            size = file.tell() / 100000

            if size > settings.max_file_size_in_mb:
                raise ValueError(
                    "File is too big, please upload something less than 15 mb"
                )

            asset = Asset(
                id=None,
                filename=filename,
                client_id=client_id,
                user_id=user_id,
                size=size,
                was_viewed=False,
                was_downloaded=False,
            )
            self.bucket_handler.upload_file(file, filename, user_id, client_id)
            self.asset_repo.create(asset)
        except Exception as e:
            print(e.__dict__)
            raise ValueError("The file upload failed.")
