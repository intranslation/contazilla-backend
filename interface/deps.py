from fastapi import Depends
from typing import Annotated, Any
from sqlalchemy.orm import Session

from infrastructure.repositories import UserRepository
from infrastructure.security import TokenHandler, PasswordHashing

from shared.database import SessionLocal


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_repo(db: Annotated[Any, Depends(get_db)]) -> UserRepository:
    return UserRepository(db=db)


def get_token_handler() -> TokenHandler:
    return TokenHandler()


def get_password_hashing() -> PasswordHashing:
    return PasswordHashing()
