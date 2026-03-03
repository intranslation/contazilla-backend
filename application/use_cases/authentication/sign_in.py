from domain.entities.user import User
from datetime import timedelta
from fastapi import HTTPException, status

from application.ports import UserRepository, PasswordHashing, TokenHandler

from shared.config import settings


class SignIn:
    def __init__(
        self,
        user_repo: UserRepository,
        password_hashing: PasswordHashing,
        token_handler: TokenHandler,
    ) -> None:
        self.user_repo = user_repo
        self.password_hashing = password_hashing
        self.token_handler = token_handler

    def execute(
        self,
        email: str,
        password: str,
    ):
        try:
            user: User | None = self.user_repo.get_user_by_email(email=email)

            if not user or not self.password_hashing.verify_password(
                password, user.password
            ):
                raise ValueError("Incorrect email or password")
        except:
            raise ValueError("Couldn't find an account with this email")

        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token: str = self.token_handler.create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )

        return {"access_token": access_token, "token_type": "bearer"}
