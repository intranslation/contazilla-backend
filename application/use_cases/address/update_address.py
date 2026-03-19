from uuid import UUID

from application.ports import AddressRepository
from domain.entities.address import Address


class UpdateAddress:
    def __init__(self, address_repo: AddressRepository) -> None:
        self.address_repo = address_repo

    def execute(
        self,
        address_id: UUID,
        street: str | None = None,
        zip_code: str | None = None,
        city: str | None = None,
        state: str | None = None,
        country: str | None = None,
        client_id: UUID | None = None,
        company_id: UUID | None = None,
    ) -> Address:
        existing = self.address_repo.get_by_id(address_id)
        if existing is None:
            raise ValueError("Address not found")

        updated_address = Address(
            id=address_id,
            street=street if street is not None else existing.street,
            zip_code=zip_code if zip_code is not None else existing.zip_code,
            city=city if city is not None else existing.city,
            state=state if state is not None else existing.state,
            country=country if country is not None else existing.country,
            client_id=client_id if client_id is not None else existing.client_id,
            company_id=company_id if company_id is not None else existing.company_id,
        )
        try:
            return self.address_repo.update(updated_address)
        except Exception:
            raise ValueError("Error while updating address")
