from uuid import UUID

from application.ports import ClientRepository


class DeleteClient:
    def __init__(self, client_repo: ClientRepository) -> None:
        self.client_repo = client_repo

    def execute(self, client_id: UUID, user_id: UUID) -> None:
        existing = self.client_repo.get_by_id(client_id, user_id)
        if existing is None:
            raise ValueError("Client not found")
        self.client_repo.delete(client_id, user_id)
