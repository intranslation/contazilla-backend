from datetime import timedelta
from typing import Protocol

from fastapi import Request


class TokenHandler(Protocol):
    def create_access_token(
        self, data: dict, expires_delta: timedelta | None = None
    ) -> str: ...
    def decode(self, token: str) -> dict: ...
