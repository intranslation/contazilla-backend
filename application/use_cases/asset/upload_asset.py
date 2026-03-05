from typing import BinaryIO
from uuid import UUID

from application.ports.asset_repository import AssetRepository
from application.ports.bucket_handler import BucketHandler
from application.ports.client_repository import ClientRepository


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
        client_id: UUID | None,
        user_id: UUID,
    ):
        # if client_id is not None:
        #     client = self.client_repo.get_by_id(client_id, user_id)

        print("print(file)")
        print(file)
        # self.bucket_handler.upload_file(file)

        try:
            self.bucket_handler.upload_file(file, filename, user_id)
        except Exception as e:
            print("Something went wrong when trying to upload the file")
            print(e.__dict__)
