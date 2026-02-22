from typing import Any
from jose import jwt
from shared.config import settings, oauth2_scheme
from datetime import datetime, timedelta, timezone


class TokenHandler:
    def get_oauth2_scheme(self):
        return oauth2_scheme

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
