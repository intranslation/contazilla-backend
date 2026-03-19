from uuid import UUID

from application.ports import AddressRepository


class DeleteAddress:
    def __init__(self, address_repo: AddressRepository) -> None:
        self.address_repo = address_repo

    def execute(self, address_id: UUID) -> None:
        existing = self.address_repo.get_by_id(address_id)
        if existing is None:
            raise ValueError("Address not found")
        self.address_repo.delete(address_id)
