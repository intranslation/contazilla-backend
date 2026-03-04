from uuid import UUID

from application.ports import CompanyRepository
from domain.entities.company import Company


class UpdateCompany:
    def __init__(self, company_repo: CompanyRepository) -> None:
        self.company_repo = company_repo

    def execute(
        self, company_id: UUID, user_id: UUID, name: str, address: str, cnpj: str, client_id: UUID | None = None
    ) -> Company:
        existing = self.company_repo.get_by_id(company_id, user_id)
        if existing is None:
            raise ValueError("Company not found")

        updated_company = Company(
            id=company_id,
            name=name,
            address=address,
            cnpj=cnpj,
            client_id=client_id,
            user_id=user_id,
        )
        try:
            return self.company_repo.update(updated_company)
        except Exception:
            raise ValueError("Error while updating company")
