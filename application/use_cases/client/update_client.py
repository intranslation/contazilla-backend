from uuid import UUID

from application.ports import ClientRepository
from domain.entities.client import Client


class UpdateClient:
    def __init__(self, client_repo: ClientRepository) -> None:
        self.client_repo = client_repo

    def execute(
        self, client_id: UUID, user_id: UUID, name: str | None, cpf: str, phone: str | None
    ) -> Client:
        existing = self.client_repo.get_by_id(client_id, user_id)
        if existing is None:
            raise ValueError("Client not found")

        updated_client = Client(
            id=client_id,
            name=name,
            cpf=cpf,
            phone=phone,
            user_id=user_id,
        )
        try:
            return self.client_repo.update(updated_client)
        except Exception:
            raise ValueError("Error while updating client")
