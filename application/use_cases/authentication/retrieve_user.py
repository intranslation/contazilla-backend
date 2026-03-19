from fastapi import HTTPException, Request, status
from jose.exceptions import JWTError

from application.ports import TokenHandler, UserRepository
from domain.entities.user import User


class RetrieveUser:
    def __init__(
        self, token: str, token_handler: TokenHandler, user_repository: UserRepository
    ):
        self.token = token
        self.token_handler = token_handler
        self.user_repository = user_repository

    def execute(self):
        email = ""
        token: str = self.token

        try:
            payload: dict = self.token_handler.decode(token)
            email: str | None = payload.get("sub")

            if email is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Credentials expired",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user = self.user_repository.get_user_by_email(email)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user
