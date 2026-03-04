from uuid import UUID
from sqlalchemy.orm import Session

from domain.entities.company import Company
from application.ports import CompanyRepository as CompanyRepositoryContract
from infrastructure.models.company import Company as CompanyModel


class CompanyRepository(CompanyRepositoryContract):
    def __init__(self, db: Session) -> None:
        self.db: Session = db

    def create(self, company: Company) -> Company:
        new_company = CompanyModel(
            name=company.name,
            address=company.address,
            cnpj=company.cnpj,
            client_id=company.client_id,
            user_id=company.user_id,
        )
        self.db.add(new_company)
        self.db.commit()
        self.db.refresh(new_company)
        return new_company.to_domain()

    def get_by_id(self, company_id: UUID, user_id: UUID) -> Company | None:
        company = (
            self.db.query(CompanyModel)
            .filter(CompanyModel.id == company_id, CompanyModel.user_id == user_id)
            .first()
        )
        if company is None:
            return None
        return company.to_domain()

    def list_by_user(self, user_id: UUID) -> list[Company]:
        companies = (
            self.db.query(CompanyModel)
            .filter(CompanyModel.user_id == user_id)
            .all()
        )
        return [c.to_domain() for c in companies]

    def update(self, company: Company) -> Company:
        db_company = (
            self.db.query(CompanyModel)
            .filter(
                CompanyModel.id == company.id,
                CompanyModel.user_id == company.user_id,
            )
            .first()
        )
        if db_company is None:
            raise ValueError("Company not found")

        db_company.name = company.name
        db_company.address = company.address
        db_company.cnpj = company.cnpj
        db_company.client_id = company.client_id
        self.db.commit()
        self.db.refresh(db_company)
        return db_company.to_domain()

    def delete(self, company_id: UUID, user_id: UUID) -> None:
        db_company = (
            self.db.query(CompanyModel)
            .filter(CompanyModel.id == company_id, CompanyModel.user_id == user_id)
            .first()
        )
        if db_company is None:
            raise ValueError("Company not found")
        self.db.delete(db_company)
        self.db.commit()

    def assign_client(self, company_id: UUID, user_id: UUID, client_id: UUID | None) -> Company:
        db_company = (
            self.db.query(CompanyModel)
            .filter(CompanyModel.id == company_id, CompanyModel.user_id == user_id)
            .first()
        )
        if db_company is None:
            raise ValueError("Company not found")
        db_company.client_id = client_id
        self.db.commit()
        self.db.refresh(db_company)
        return db_company.to_domain()
