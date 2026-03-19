from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import Request
from jose import jwt

from application.ports import TokenHandler as TokenHandlerContract
from shared.config import oauth2_scheme, settings


class TokenHandler(TokenHandlerContract):
    def create_access_token(
        self, data: dict, expires_delta: timedelta | None = None
    ) -> str:
        to_encode: dict[Any, Any] = data.copy()
        if expires_delta:
            expire: datetime = datetime.now(timezone.utc) + expires_delta
        else:
            expire: datetime = datetime.now(timezone.utc) + timedelta(
                minutes=settings.access_token_expire_minutes
            )
        to_encode.update({"exp": expire})
        encoded_jwt: str = jwt.encode(
            to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm
        )
        return encoded_jwt

    def decode(self, token: str) -> dict:
        return jwt.decode(
            token, settings.jwt_secret, algorithms=[settings.jwt_algorithm]
        )
