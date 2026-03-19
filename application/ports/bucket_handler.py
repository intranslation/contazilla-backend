from typing import Any, BinaryIO, Protocol
from uuid import UUID


class BucketHandler(Protocol):
    def retrieve_file(self, key: str) -> Any: ...
    def upload_file(
        self, file: BinaryIO, filename: str, user_id: UUID, client_id: UUID
    ) -> str: ...
