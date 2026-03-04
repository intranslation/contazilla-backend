from uuid import UUID

from application.ports import CompanyRepository


class DeleteCompany:
    def __init__(self, company_repo: CompanyRepository) -> None:
        self.company_repo = company_repo

    def execute(self, company_id: UUID, user_id: UUID) -> None:
        existing = self.company_repo.get_by_id(company_id, user_id)
        if existing is None:
            raise ValueError("Company not found")
        self.company_repo.delete(company_id, user_id)
