from botocore.exceptions import ClientError
from typing import BinaryIO, Any
from uuid import UUID
from infrastructure.exceptions import R2UploadErrorException
from shared.config import settings
import boto3


from application.ports.bucket_handler import BucketHandler as BucketHandlerInterface


class BucketHandler(BucketHandlerInterface):
    def __init__(self):
        self.client = boto3.client(
            service_name="s3",
            endpoint_url=settings.r2_endpoint,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.region_name,
        )

    def retrieve_file(self, key: str) -> Any:
        try:
            obj = self.client.get_object(Bucket=settings.r2_bucket, Key=key)
        except ClientError as e:
            code = e.response.get("Error", {}).get("Code", "Unknown")
            if code in ("NoSuchKey", "404"):
                raise ValueError("File not found")
            if code in ("AccessDenied", "403"):
                raise ValueError("Access denied")
            print(e.__dict__)
            raise ValueError(f"S3 error: {code}")

        return obj

    def upload_file(self, file: BinaryIO, filename: str, user_id: UUID) -> str:
        try:
            url = self.client.upload_fileobj(
                Fileobj=file,
                Bucket=settings.r2_bucket,
                Key=f"{str(user_id)}/{filename}",
            )
        except:
            raise R2UploadErrorException()
        return url
