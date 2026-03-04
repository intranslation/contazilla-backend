from interface.deps.database import get_db
from fastapi import Depends
from typing import Annotated, Any

from infrastructure.repositories.company import CompanyRepository
from infrastructure.repositories.client import ClientRepository
from application.use_cases.company import (
    CreateCompany,
    GetCompany,
    ListCompanies,
    UpdateCompany,
    DeleteCompany,
    AssignClientToCompany,
)


def get_company_repo(db: Annotated[Any, Depends(get_db)]) -> CompanyRepository:
    return CompanyRepository(db=db)


def create_company_use_case(
    company_repository: Annotated[CompanyRepository, Depends(get_company_repo)],
):
    return CreateCompany(company_repo=company_repository)


def get_company_use_case(
    company_repository: Annotated[CompanyRepository, Depends(get_company_repo)],
):
    return GetCompany(company_repo=company_repository)


def list_companies_use_case(
    company_repository: Annotated[CompanyRepository, Depends(get_company_repo)],
):
    return ListCompanies(company_repo=company_repository)


def update_company_use_case(
    company_repository: Annotated[CompanyRepository, Depends(get_company_repo)],
):
    return UpdateCompany(company_repo=company_repository)


def delete_company_use_case(
    company_repository: Annotated[CompanyRepository, Depends(get_company_repo)],
):
    return DeleteCompany(company_repo=company_repository)


def get_client_repo_for_company(db: Annotated[Any, Depends(get_db)]) -> ClientRepository:
    return ClientRepository(db=db)


def assign_client_to_company_use_case(
    company_repository: Annotated[CompanyRepository, Depends(get_company_repo)],
    client_repository: Annotated[ClientRepository, Depends(get_client_repo_for_company)],
):
    return AssignClientToCompany(company_repo=company_repository, client_repo=client_repository)
