from uuid import UUID

from application.ports import ClientRepository
from domain.entities.client import Client


class CreateClient:
    def __init__(self, client_repo: ClientRepository) -> None:
        self.client_repo = client_repo

    def execute(
        self,
        name: str,
        cpf: str | None,
        phone: str | None,
        email: str | None,
        user_id: UUID,
        is_premium: bool = False,
    ) -> Client:
        new_client = Client(
            id=None,
            name=name,
            email=email,
            cpf=cpf,
            phone=phone,
            user_id=user_id,
            is_premium=is_premium,
        )
        try:
            return self.client_repo.create(new_client)
        except Exception:
            raise ValueError("Error while creating client")
