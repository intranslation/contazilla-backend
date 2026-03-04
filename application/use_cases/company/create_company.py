from uuid import UUID

from application.ports import CompanyRepository
from domain.entities.company import Company


class CreateCompany:
    def __init__(self, company_repo: CompanyRepository) -> None:
        self.company_repo = company_repo

    def execute(self, name: str, address: str, cnpj: str, user_id: UUID, client_id: UUID | None = None) -> Company:
        new_company = Company(
            id=None,
            name=name,
            address=address,
            cnpj=cnpj,
            client_id=client_id,
            user_id=user_id,
        )
        try:
            return self.company_repo.create(new_company)
        except Exception:
            raise ValueError("Error while creating company")
