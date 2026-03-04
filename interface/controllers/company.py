from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from application.use_cases.company import (
    CreateCompany,
    GetCompany,
    ListCompanies,
    UpdateCompany,
    DeleteCompany,
    AssignClientToCompany,
)
from domain.entities.user import User
from interface.deps import (
    get_current_user_use_case,
    create_company_use_case,
    get_company_use_case,
    list_companies_use_case,
    update_company_use_case,
    delete_company_use_case,
    assign_client_to_company_use_case,
)
from interface.schemas import CompanyCreate, CompanyUpdate, CompanyResponse, AssignClient

router = APIRouter(prefix="/companies", tags=["companies"])


@router.post("/", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
def create(
    data: CompanyCreate,
    current_user: Annotated[User, Depends(get_current_user_use_case)],
    use_case: Annotated[CreateCompany, Depends(create_company_use_case)],
):
    try:
        company = use_case.execute(
            name=data.name,
            address=data.address,
            cnpj=data.cnpj,
            user_id=current_user.id,
            client_id=UUID(data.client_id) if data.client_id else None,
        )
        return CompanyResponse(
            id=str(company.id),
            name=company.name,
            address=company.address,
            cnpj=company.cnpj,
            client_id=str(company.client_id) if company.client_id else None,
            user_id=str(company.user_id),
        )
    except ValueError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e))


@router.get("/", response_model=list[CompanyResponse])
def list_all(
    current_user: Annotated[User, Depends(get_current_user_use_case)],
    use_case: Annotated[ListCompanies, Depends(list_companies_use_case)],
):
    companies = use_case.execute(user_id=current_user.id)
    return [
        CompanyResponse(
            id=str(c.id),
            name=c.name,
            address=c.address,
            cnpj=c.cnpj,
            client_id=str(c.client_id) if c.client_id else None,
            user_id=str(c.user_id),
        )
        for c in companies
    ]


@router.get("/{company_id}", response_model=CompanyResponse)
def get_by_id(
    company_id: UUID,
    current_user: Annotated[User, Depends(get_current_user_use_case)],
    use_case: Annotated[GetCompany, Depends(get_company_use_case)],
):
    try:
        company = use_case.execute(company_id=company_id, user_id=current_user.id)
        return CompanyResponse(
            id=str(company.id),
            name=company.name,
            address=company.address,
            cnpj=company.cnpj,
            client_id=str(company.client_id) if company.client_id else None,
            user_id=str(company.user_id),
        )
    except ValueError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e))


@router.put("/{company_id}", response_model=CompanyResponse)
def update(
    company_id: UUID,
    data: CompanyUpdate,
    current_user: Annotated[User, Depends(get_current_user_use_case)],
    use_case: Annotated[UpdateCompany, Depends(update_company_use_case)],
):
    try:
        company = use_case.execute(
            company_id=company_id,
            user_id=current_user.id,
            name=data.name,
            address=data.address,
            cnpj=data.cnpj,
            client_id=UUID(data.client_id) if data.client_id else None,
        )
        return CompanyResponse(
            id=str(company.id),
            name=company.name,
            address=company.address,
            cnpj=company.cnpj,
            client_id=str(company.client_id) if company.client_id else None,
            user_id=str(company.user_id),
        )
    except ValueError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e))


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    company_id: UUID,
    current_user: Annotated[User, Depends(get_current_user_use_case)],
    use_case: Annotated[DeleteCompany, Depends(delete_company_use_case)],
):
    try:
        use_case.execute(company_id=company_id, user_id=current_user.id)
    except ValueError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e))


@router.patch("/{company_id}/client", response_model=CompanyResponse)
def assign_client(
    company_id: UUID,
    data: AssignClient,
    current_user: Annotated[User, Depends(get_current_user_use_case)],
    use_case: Annotated[AssignClientToCompany, Depends(assign_client_to_company_use_case)],
):
    try:
        company = use_case.execute(
            company_id=company_id,
            user_id=current_user.id,
            client_id=UUID(data.client_id) if data.client_id else None,
        )
        return CompanyResponse(
            id=str(company.id),
            name=company.name,
            address=company.address,
            cnpj=company.cnpj,
            client_id=str(company.client_id) if company.client_id else None,
            user_id=str(company.user_id),
        )
    except ValueError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e))
