from uuid import UUID

from application.ports import CompanyRepository
from domain.entities.company import Company


class ListCompanies:
    def __init__(self, company_repo: CompanyRepository) -> None:
        self.company_repo = company_repo

    def execute(self, user_id: UUID) -> list[Company]:
        return self.company_repo.list_by_user(user_id)
