from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from application.ports.repositories.authentication import AuthenticationRepository
from application.services.hashing_utilities import HashingUtilitiesService
from domain.entities.user import User
from interface.deps import get_auth_repo, get_hash_utilities, get_current_user
from interface.schemas import Token, UserCreate, UserResponse

from application.use_cases import RegisterUser, SignIn

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def register(
    user_data: UserCreate,
    auth_repo: Annotated[AuthenticationRepository, Depends(get_auth_repo)],
    hash_service: Annotated[HashingUtilitiesService, Depends(get_hash_utilities)],
):
    return RegisterUser.execute(
        auth_repo=auth_repo,
        hash_service=hash_service,
        email=user_data.email,
        name=user_data.name,
        phone=user_data.phone,
        password=user_data.password,
    )


@router.post("/login", response_model=Token)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_repo: Annotated[AuthenticationRepository, Depends(get_auth_repo)],
    hash_service: Annotated[HashingUtilitiesService, Depends(get_hash_utilities)],
):
    return SignIn.execute(
        auth_repo=auth_repo,
        hash_service=hash_service,
        email=form_data.username,
        password=form_data.password,
    )


@router.get("/me", response_model=UserResponse)
def get_me(
    user: Annotated[User, Depends(get_current_user)],
):
    return user
