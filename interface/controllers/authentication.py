from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from application.use_cases import RegisterUser, RetrieveUser, SignIn
from application.use_cases.authentication.register_client_user import RegisterClientUser
from domain.entities.user import User
from domain.enums.role import UserRole
from interface.deps import (
    get_retrieve_user_use_case,
    register_use_case,
    sign_in_use_case,
)
from interface.deps.authentication import (
    get_current_user_use_case,
    register_client_use_case,
)
from interface.schemas import Token, UserCreate, UserRegisterResponse, UserResponse
from interface.schemas.user import CreateClientUserBody

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=UserRegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user_data: UserCreate,
    use_case: Annotated[RegisterUser, Depends(register_use_case)],
):
    try:
        user = use_case.execute(
            email=user_data.email,
            name=user_data.name,
            phone=user_data.phone,
            password=user_data.password,
        )
        serialized = UserRegisterResponse(
            email=user.email, name=user.name, phone=user.phone
        )
    except ValueError as e:
        raise HTTPException(400, str(e))
    return serialized


@router.post(
    "/register-client",
    response_model=UserRegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_client(
    body: CreateClientUserBody,
    current_user: Annotated[User, Depends(get_current_user_use_case)],
    use_case: Annotated[RegisterClientUser, Depends(register_client_use_case)],
):
    try:
        user = use_case.execute(
            client_id=body.client_id,
            temp_password=body.temp_password,
            user_id=current_user.id,
        )
        serialized = UserRegisterResponse(
            email=user.email, name=user.name, phone=user.phone
        )
    except ValueError as e:
        raise HTTPException(400, str(e))
    return serialized


@router.post("/login", response_model=Token)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    use_case: Annotated[SignIn, Depends(sign_in_use_case)],
):
    try:
        token = use_case.execute(
            email=form_data.username,
            password=form_data.password,
        )
    except ValueError as e:
        raise HTTPException(404, str(e))
    return Token(access_token=token["access_token"], token_type=token["token_type"])


@router.get("/me", response_model=UserResponse)
def get_me(
    use_case: Annotated[RetrieveUser, Depends(get_retrieve_user_use_case)],
):
    user = use_case.execute()
    serialized = UserResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        phone=user.phone,
        is_client=user.role == UserRole.CLIENT,
    )
    return serialized
