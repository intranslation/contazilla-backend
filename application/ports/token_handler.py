from fastapi import Request
from typing import Protocol
from datetime import timedelta


class TokenHandler(Protocol):
    def create_access_token(
        self, data: dict, expires_delta: timedelta | None = None
    ) -> str: ...
    def decode(self, token: str) -> dict: ...
