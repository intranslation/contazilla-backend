from domain.entities.user import User
from jose.exceptions import JWTError
from fastapi import HTTPException, status, Request

from application.ports import UserRepository, TokenHandler


class RetrieveUser:
    def __init__(
        self, token: str, token_handler: TokenHandler, user_repository: UserRepository
    ):
        self.token = token
        self.token_handler = token_handler
        self.user_repository = user_repository

    def execute(self):
        print("Hi")

        email = ""
        token: str = self.token

        try:
            payload: dict = self.token_handler.decode(token)
            email: str | None = payload.get("sub")

            if email is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
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

        print(user)

        return user
