from uuid import UUID

from application.ports import AddressRepository
from domain.entities.address import Address


class ListAddresses:
    def __init__(self, address_repo: AddressRepository) -> None:
        self.address_repo = address_repo

    def execute(
        self,
        user_id: UUID | None = None,
        client_id: UUID | None = None,
        company_id: UUID | None = None,
    ) -> list[Address]:
        if client_id is not None:
            return self.address_repo.list_by_client(client_id)
        if company_id is not None:
            return self.address_repo.list_by_company(company_id)
        if user_id is not None:
            return self.address_repo.list_by_user(user_id)
        return []
