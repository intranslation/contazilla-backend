from uuid import UUID

from application.ports import CompanyRepository
from domain.entities.company import Company


class GetCompany:
    def __init__(self, company_repo: CompanyRepository) -> None:
        self.company_repo = company_repo

    def execute(self, company_id: UUID, user_id: UUID) -> Company:
        company = self.company_repo.get_by_id(company_id, user_id)
        if company is None:
            raise ValueError("Company not found")
        return company
