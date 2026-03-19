from uuid import UUID

from application.ports import AddressRepository
from domain.entities.address import Address


class CreateAddress:
    def __init__(self, address_repo: AddressRepository) -> None:
        self.address_repo = address_repo

    def execute(
        self,
        street: str | None,
        zip_code: str | None,
        city: str | None,
        state: str | None,
        country: str | None,
        client_id: UUID | None = None,
        company_id: UUID | None = None,
    ) -> Address:
        new_address = Address(
            id=None,
            street=street,
            zip_code=zip_code,
            city=city,
            state=state,
            country=country,
            client_id=client_id,
            company_id=company_id,
        )
        try:
            return self.address_repo.create(new_address)
        except Exception as e:
            print("print(e)")
            print(e)
            raise ValueError(e)
