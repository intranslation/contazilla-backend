from typing import Protocol, BinaryIO, Any
from uuid import UUID


class BucketHandler(Protocol):
    def retrieve_file(self, key: str) -> Any: ...
    def upload_file(self, file: BinaryIO, filename: str, user_id: UUID) -> str: ...
