from domain.entities.user import User
from shared.config import oauth2_scheme
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Annotated
from shared.database import SessionLocal
from application.services import HashingUtilitiesService
from infrastructure.repositories import AuthenticationRepository


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_hash_utilities() -> HashingUtilitiesService:
    return HashingUtilitiesService()


def get_current_user(
    hash_utilities: Annotated[HashingUtilitiesService, Depends(get_hash_utilities)],
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    return hash_utilities.get_current_user(token, db)


def get_auth_repo() -> AuthenticationRepository:
    session: Session = get_db()
    return AuthenticationRepository(db=session)
