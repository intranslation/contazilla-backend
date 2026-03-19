from typing import Annotated, Any

from fastapi import Depends

from application.use_cases.client import (CreateClient, DeleteClient,
                                          GetClient, ListClients, UpdateClient)
from infrastructure.repositories.client import ClientRepository
from interface.deps.database import get_db


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
