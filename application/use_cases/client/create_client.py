from uuid import UUID

from application.ports import ClientRepository
from domain.entities.client import Client


class CreateClient:
    def __init__(self, client_repo: ClientRepository) -> None:
        self.client_repo = client_repo

    def execute(self, name: str | None, cpf: str, phone: str | None, user_id: UUID) -> Client:
        new_client = Client(
            id=None,
            name=name,
            cpf=cpf,
            phone=phone,
            user_id=user_id,
        )
        try:
            return self.client_repo.create(new_client)
        except Exception:
            raise ValueError("Error while creating client")
