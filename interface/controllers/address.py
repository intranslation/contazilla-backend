from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from application.use_cases.address import (CreateAddress, DeleteAddress,
                                           ListAddresses, UpdateAddress)
from domain.entities.user import User
from interface.deps import (create_address_use_case, delete_address_use_case,
                            get_current_user_use_case, list_addresses_use_case,
                            update_address_use_case)
from interface.schemas import AddressCreate, AddressResponse, AddressUpdate

router = APIRouter(prefix="/addresses", tags=["addresses"])


def _to_response(addr) -> AddressResponse:
    return AddressResponse(
        id=str(addr.id),
        street=addr.street,
        zip_code=addr.zip_code,
        city=addr.city,
        state=addr.state,
        country=addr.country,
        client_id=str(addr.client_id) if addr.client_id else None,
        company_id=str(addr.company_id) if addr.company_id else None,
    )


@router.get("/", response_model=list[AddressResponse])
def list_all(
    current_user: Annotated[User, Depends(get_current_user_use_case)],
    use_case: Annotated[ListAddresses, Depends(list_addresses_use_case)],
    client_id: UUID | None = Query(default=None),
    company_id: UUID | None = Query(default=None),
):
    addresses = use_case.execute(
        user_id=current_user.id,
        client_id=client_id,
        company_id=company_id,
    )
    return [_to_response(a) for a in addresses]


@router.post("/", response_model=AddressResponse, status_code=status.HTTP_201_CREATED)
def create(
    data: AddressCreate,
    current_user: Annotated[User, Depends(get_current_user_use_case)],
    use_case: Annotated[CreateAddress, Depends(create_address_use_case)],
):
    try:
        address = use_case.execute(
            street=data.street,
            zip_code=data.zip_code,
            city=data.city,
            state=data.state,
            country=data.country,
            client_id=UUID(data.client_id) if data.client_id else None,
            company_id=UUID(data.company_id) if data.company_id else None,
        )
        return _to_response(address)
    except ValueError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e))


@router.patch("/{address_id}", response_model=AddressResponse)
def update(
    address_id: UUID,
    data: AddressUpdate,
    current_user: Annotated[User, Depends(get_current_user_use_case)],
    use_case: Annotated[UpdateAddress, Depends(update_address_use_case)],
):
    try:
        address = use_case.execute(
            address_id=address_id,
            street=data.street,
            zip_code=data.zip_code,
            city=data.city,
            state=data.state,
            country=data.country,
            client_id=UUID(data.client_id) if data.client_id else None,
            company_id=UUID(data.company_id) if data.company_id else None,
        )
        return _to_response(address)
    except ValueError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e))


@router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    address_id: UUID,
    current_user: Annotated[User, Depends(get_current_user_use_case)],
    use_case: Annotated[DeleteAddress, Depends(delete_address_use_case)],
):
    try:
        use_case.execute(address_id=address_id)
    except ValueError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e))
