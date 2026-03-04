from interface.deps.database import get_db
from fastapi import Depends
from typing import Annotated, Any

from infrastructure.repositories.client import ClientRepository
from application.use_cases.client import (
    CreateClient,
    GetClient,
    ListClients,
    UpdateClient,
    DeleteClient,
)


def get_client_repo(db: Annotated[Any, Depends(get_db)]) -> ClientRepository:
    return ClientRepository(db=db)


def create_client_use_case(
    client_repository: Annotated[ClientRepository, Depends(get_client_repo)],
):
    return CreateClient(client_repo=client_repository)


def get_client_use_case(
    client_repository: Annotated[ClientRepository, Depends(get_client_repo)],
):
    return GetClient(client_repo=client_repository)


def list_clients_use_case(
    client_repository: Annotated[ClientRepository, Depends(get_client_repo)],
):
    return ListClients(client_repo=client_repository)


def update_client_use_case(
    client_repository: Annotated[ClientRepository, Depends(get_client_repo)],
):
    return UpdateClient(client_repo=client_repository)


def delete_client_use_case(
    client_repository: Annotated[ClientRepository, Depends(get_client_repo)],
):
    return DeleteClient(client_repo=client_repository)
