from uuid import UUID

from application.ports import ClientRepository
from domain.entities.client import Client


class GetClient:
    def __init__(self, client_repo: ClientRepository) -> None:
        self.client_repo = client_repo

    def execute(self, client_id: UUID, user_id: UUID) -> Client:
        client = self.client_repo.get_by_id(client_id, user_id)
        if client is None:
            raise ValueError("Client not found")
        return client
