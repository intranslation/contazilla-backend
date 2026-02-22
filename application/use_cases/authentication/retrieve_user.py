from domain.entities.user import User
from jose.exceptions import JWTError
from fastapi import HTTPException, status

from application.ports import UserRepository, TokenHandler


class RetrieveUser:
    @staticmethod
    def execute(token_handler: TokenHandler, user_repository: UserRepository):
        email = ""
        token: str = token_handler.get_oauth2_scheme()

        try:
            payload: dict = token_handler.decode(token)
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

        user: User | None = user_repository.get_user_by_email(email)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user
