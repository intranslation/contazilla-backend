from uuid import UUID

from sqlalchemy.exc import SQLAlchemyError

from application.ports import AddressRepository, CompanyRepository
from domain.entities.company import Company


class CreateCompany:
    def __init__(self, company_repo: CompanyRepository, address_repo: AddressRepository) -> None:
        self.company_repo = company_repo
        self.address_repo = address_repo

    def execute(
        self,
        name: str,
        address_id: UUID | None,
        cnpj: str,
        user_id: UUID,
        client_id: UUID | None = None,
    ) -> Company:
        address = None
        if address_id:
            address = self.address_repo.get_by_id(address_id)
            if address is None:
                raise ValueError("Address not found")

        new_company = Company(
            id=None,
            name=name,
            address=address,
            cnpj=cnpj,
            client_id=client_id,
            user_id=user_id,
        )
        try:
            created = self.company_repo.create(new_company)
            if address_id and address and created.id:
                address.company_id = created.id
                self.address_repo.update(address)
            result = self.company_repo.get_by_id(created.id, user_id)
            if result is None:
                raise ValueError("Failed to retrieve created company")
            return result
        except SQLAlchemyError as e:
            print(f"[CreateCompany] Database error: {e}")
            raise ValueError("Error while creating company")
        except Exception as e:
            print(f"[CreateCompany] Unexpected error: {e}")
            raise ValueError("Error while creating company")
