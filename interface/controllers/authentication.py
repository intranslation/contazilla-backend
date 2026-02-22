from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from application.ports.password_hashing import PasswordHashing
from application.ports.token_handler import TokenHandler
from application.use_cases.authentication.retrieve_user import RetrieveUser
from interface.deps import get_user_repo, get_password_hashing, get_token_handler
from interface.schemas import Token, UserCreate, UserResponse

from application.ports import UserRepository
from application.use_cases import RegisterUser, SignIn

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def register(
    user_data: UserCreate,
    user_repo: Annotated[UserRepository, Depends(get_user_repo)],
    password_hashing: Annotated[PasswordHashing, Depends(get_password_hashing)],
):
    return RegisterUser.execute(
        user_repo=user_repo,
        password_hashing=password_hashing,
        email=user_data.email,
        name=user_data.name,
        phone=user_data.phone,
        password=user_data.password,
    )


@router.post("/login", response_model=Token)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    token_handler: Annotated[TokenHandler, Depends(get_token_handler)],
    password_hashing: Annotated[PasswordHashing, Depends(get_password_hashing)],
    user_repo: Annotated[UserRepository, Depends(get_user_repo)],
):
    return SignIn.execute(
        user_repo=user_repo,
        password_hashing=password_hashing,
        token_handler=token_handler,
        email=form_data.username,
        password=form_data.password,
    )


@router.get("/me", response_model=UserResponse)
def get_me(
    token_handler: Annotated[TokenHandler, Depends(get_token_handler)],
    user_repository: Annotated[UserRepository, Depends(get_user_repo)],
):
    return UserResponse.model_validate(
        RetrieveUser.execute(
            token_handler=token_handler, user_repository=user_repository
        )
    )
