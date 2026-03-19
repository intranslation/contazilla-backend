from uuid import UUID

from application.ports import ClientRepository
from domain.entities.client import Client


class UpdateClient:
    def __init__(self, client_repo: ClientRepository) -> None:
        self.client_repo = client_repo

    def execute(
        self,
        client_id: UUID,
        user_id: UUID,
        name: str | None,
        cpf: str | None,
        email: str | None,
        phone: str | None,
        is_premium: bool | None = None,
    ) -> Client:
        existing = self.client_repo.get_by_id(client_id, user_id)
        if existing is None:
            raise ValueError("Client not found")

        updated_client = Client(
            id=client_id,
            name=name,
            cpf=cpf,
            email=email,
            phone=phone,
            user_id=user_id,
            is_premium=is_premium if is_premium is not None else existing.is_premium,
        )
        try:
            return self.client_repo.update(updated_client)
        except Exception:
            raise ValueError("Error while updating client")
