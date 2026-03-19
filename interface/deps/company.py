from typing import Annotated, Any

from fastapi import Depends

from application.use_cases.company import (AssignClientToCompany,
                                           CreateCompany, DeleteCompany,
                                           GetCompany, ListCompanies,
                                           UpdateCompany)
from infrastructure.repositories.address import AddressRepository
from infrastructure.repositories.client import ClientRepository
from infrastructure.repositories.company import CompanyRepository
from interface.deps.database import get_db


def get_company_repo(db: Annotated[Any, Depends(get_db)]) -> CompanyRepository:
    return CompanyRepository(db=db)


def get_address_repo_for_company(db: Annotated[Any, Depends(get_db)]) -> AddressRepository:
    return AddressRepository(db=db)


def create_company_use_case(
    company_repository: Annotated[CompanyRepository, Depends(get_company_repo)],
    address_repository: Annotated[AddressRepository, Depends(get_address_repo_for_company)],
):
    return CreateCompany(company_repo=company_repository, address_repo=address_repository)


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
    address_repository: Annotated[AddressRepository, Depends(get_address_repo_for_company)],
):
    return UpdateCompany(company_repo=company_repository, address_repo=address_repository)


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
