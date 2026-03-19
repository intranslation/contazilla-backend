from typing import Annotated, Any

from fastapi import Depends

from application.use_cases.address import (CreateAddress, DeleteAddress,
                                           ListAddresses, UpdateAddress)
from infrastructure.repositories.address import AddressRepository
from interface.deps.database import get_db


def get_address_repo(db: Annotated[Any, Depends(get_db)]) -> AddressRepository:
    return AddressRepository(db=db)


def create_address_use_case(
    address_repository: Annotated[AddressRepository, Depends(get_address_repo)],
):
    return CreateAddress(address_repo=address_repository)


def list_addresses_use_case(
    address_repository: Annotated[AddressRepository, Depends(get_address_repo)],
):
    return ListAddresses(address_repo=address_repository)


def update_address_use_case(
    address_repository: Annotated[AddressRepository, Depends(get_address_repo)],
):
    return UpdateAddress(address_repo=address_repository)


def delete_address_use_case(
    address_repository: Annotated[AddressRepository, Depends(get_address_repo)],
):
    return DeleteAddress(address_repo=address_repository)
