from typing import Annotated

from fastapi import Depends

from application.use_cases import RegisterUser, RetrieveUser, SignIn
from application.use_cases.authentication.register_client_user import \
    RegisterClientUser
from infrastructure.repositories.client import ClientRepository
from infrastructure.repositories.user import UserRepository
from infrastructure.security.password_hashing import PasswordHashing
from infrastructure.security.token_handler import TokenHandler
from interface.deps.client import get_client_repo
from interface.deps.tokens import (get_oauth2_scheme, get_password_hashing,
                                   get_token_handler)
from interface.deps.user import get_user_repo


def get_retrieve_user_use_case(
    token: Annotated[str, Depends(get_oauth2_scheme)],
    token_handler: Annotated[TokenHandler, Depends(get_token_handler)],
    user_repository: Annotated[UserRepository, Depends(get_user_repo)],
):
    use_case = RetrieveUser(
        token=token, token_handler=token_handler, user_repository=user_repository
    )
    return use_case


def get_current_user_use_case(
    use_case: Annotated[RetrieveUser, Depends(get_retrieve_user_use_case)],
):
    return use_case.execute()


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


def register_client_use_case(
    password_hashing: Annotated[PasswordHashing, Depends(get_password_hashing)],
    user_repository: Annotated[UserRepository, Depends(get_user_repo)],
    client_repository: Annotated[ClientRepository, Depends(get_client_repo)],
):
    use_case = RegisterClientUser(
        user_repo=user_repository,
        client_repo=client_repository,
        password_hashing=password_hashing,
    )
    return use_case
