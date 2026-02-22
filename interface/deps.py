from shared.config import oauth2_scheme
from fastapi import Depends
from typing import Annotated, Any
from sqlalchemy.orm import Session

from application.use_cases import RetrieveUser, SignIn, RegisterUser
from infrastructure.repositories import UserRepository
from infrastructure.security import TokenHandler, PasswordHashing

from shared.database import SessionLocal


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_oauth2_scheme(token: Annotated[str, Depends(oauth2_scheme)]):
    return token


def get_user_repo(db: Annotated[Any, Depends(get_db)]) -> UserRepository:
    return UserRepository(db=db)


def get_token_handler() -> TokenHandler:
    return TokenHandler()


def get_password_hashing() -> PasswordHashing:
    return PasswordHashing()


def get_retrieve_user_use_case(
    token: Annotated[str, Depends(get_oauth2_scheme)],
    token_handler: Annotated[TokenHandler, Depends(get_token_handler)],
    user_repository: Annotated[UserRepository, Depends(get_user_repo)],
):
    use_case = RetrieveUser(
        token=token, token_handler=token_handler, user_repository=user_repository
    )
    return use_case


def sign_in_use_case(
    password_hashing: Annotated[PasswordHashing, Depends(get_password_hashing)],
    token_handler: Annotated[TokenHandler, Depends(get_token_handler)],
    user_repository: Annotated[UserRepository, Depends(get_user_repo)],
):
    use_case = SignIn(
        token_handler=token_handler,
        user_repo=user_repository,
        password_hashing=password_hashing,
    )
    return use_case


def register_use_case(
    password_hashing: Annotated[PasswordHashing, Depends(get_password_hashing)],
    user_repository: Annotated[UserRepository, Depends(get_user_repo)],
):
    use_case = RegisterUser(
        user_repo=user_repository,
        password_hashing=password_hashing,
    )
    return use_case
