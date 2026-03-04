from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from interface.deps import (
    get_retrieve_user_use_case,
    sign_in_use_case,
    register_use_case,
)
from interface.schemas import Token, UserCreate, UserResponse
from application.use_cases import RegisterUser, SignIn, RetrieveUser

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
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
        serialized = UserResponse(
            id=str(user.id), email=user.email, name=user.name, phone=user.phone
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
        print("TOKEN")
        print(token)
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
    )
    return serialized
