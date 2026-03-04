from uuid import UUID

from application.ports import CompanyRepository, ClientRepository
from domain.entities.company import Company


class AssignClientToCompany:
    def __init__(self, company_repo: CompanyRepository, client_repo: ClientRepository) -> None:
        self.company_repo = company_repo
        self.client_repo = client_repo

    def execute(self, company_id: UUID, user_id: UUID, client_id: UUID | None) -> Company:
        existing = self.company_repo.get_by_id(company_id, user_id)
        if existing is None:
            raise ValueError("Company not found")

        if client_id is not None:
            client = self.client_repo.get_by_id(client_id, user_id)
            if client is None:
                raise ValueError("Client not found")

        return self.company_repo.assign_client(company_id, user_id, client_id)
