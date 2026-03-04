from infrastructure.security import TokenHandler
from infrastructure.security.password_hashing import PasswordHashing
from shared.config import oauth2_scheme
from fastapi import Depends
from typing import Annotated


def get_oauth2_scheme(token: Annotated[str, Depends(oauth2_scheme)]):
    return token


def get_token_handler() -> TokenHandler:
    return TokenHandler()


def get_password_hashing() -> PasswordHashing:
    return PasswordHashing()
