from domain.entities.user import User
from datetime import timedelta
from fastapi import HTTPException, status

from application.ports import UserRepository, PasswordHashing, TokenHandler

from shared.config import settings


class SignIn:
    @staticmethod
    def execute(
        user_repo: UserRepository,
        password_hashing: PasswordHashing,
        token_handler: TokenHandler,
        email: str,
        password: str,
    ):
        user: User | None = user_repo.get_user_by_email(email=email)

        if not user or not password_hashing.verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token: str = token_handler.create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )

        return {"access_token": access_token, "token_type": "bearer"}
