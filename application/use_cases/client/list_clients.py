from uuid import UUID

from application.ports import ClientRepository
from domain.entities.client import Client


class ListClients:
    def __init__(self, client_repo: ClientRepository) -> None:
        self.client_repo = client_repo

    def execute(self, user_id: UUID) -> list[Client]:
        return self.client_repo.list_by_user(user_id)
