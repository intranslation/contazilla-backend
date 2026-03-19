from typing import Annotated, Any

from fastapi import Depends

from infrastructure.repositories.user import UserRepository
from interface.deps.database import get_db


def get_user_repo(db: Annotated[Any, Depends(get_db)]) -> UserRepository:
    return UserRepository(db=db)
