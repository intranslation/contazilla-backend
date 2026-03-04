from typing import Annotated
from fastapi import APIRouter, Depends

from application.use_cases.authentication.retrieve_user import RetrieveUser
from interface.deps import get_current_user_use_case

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/")
def test_guard(
    current_user: Annotated[RetrieveUser, Depends(get_current_user_use_case)],
):
    return "this works!"
