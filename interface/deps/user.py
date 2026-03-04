from interface.deps.database import get_db
from fastapi import Depends
from typing import Annotated, Any

from infrastructure.repositories.user import UserRepository


def get_user_repo(db: Annotated[Any, Depends(get_db)]) -> UserRepository:
    return UserRepository(db=db)
