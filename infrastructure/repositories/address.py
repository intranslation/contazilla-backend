from uuid import UUID

from sqlalchemy import or_
from sqlalchemy.orm import Session

from application.ports import AddressRepository as AddressRepositoryContract
from domain.entities.address import Address
from infrastructure.models.address import Address as AddressModel
from infrastructure.models.client import Client as ClientModel
from infrastructure.models.company import Company as CompanyModel


class AddressRepository(AddressRepositoryContract):
    def __init__(self, db: Session) -> None:
        self.db: Session = db

    def create(self, address: Address) -> Address:
        new_address = AddressModel(
            street=address.street,
            zip_code=address.zip_code,
            city=address.city,
            state=address.state,
            country=address.country,
            client_id=address.client_id,
            company_id=address.company_id,
        )
        self.db.add(new_address)
        self.db.commit()
        self.db.refresh(new_address)
        return new_address.to_domain()

    def get_by_id(self, address_id: UUID) -> Address | None:
        address = (
            self.db.query(AddressModel).filter(AddressModel.id == address_id).first()
        )
        if address is None:
            return None
        return address.to_domain()

    def list_by_user(self, user_id: UUID) -> list[Address]:
        client_ids = self.db.query(ClientModel.id).filter(
            ClientModel.user_id == user_id
        )
        company_ids = self.db.query(CompanyModel.id).filter(
            CompanyModel.user_id == user_id
        )
        addresses = (
            self.db.query(AddressModel)
            .filter(
                or_(
                    AddressModel.client_id.in_(client_ids),
                    AddressModel.company_id.in_(company_ids),
                )
            )
            .all()
        )
        return [a.to_domain() for a in addresses]

    def list_by_client(self, client_id: UUID) -> list[Address]:
        addresses = (
            self.db.query(AddressModel)
            .filter(AddressModel.client_id == client_id)
            .all()
        )
        return [a.to_domain() for a in addresses]

    def list_by_company(self, company_id: UUID) -> list[Address]:
        addresses = (
            self.db.query(AddressModel)
            .filter(AddressModel.company_id == company_id)
            .all()
        )
        return [a.to_domain() for a in addresses]

    def update(self, address: Address) -> Address:
        db_address = (
            self.db.query(AddressModel).filter(AddressModel.id == address.id).first()
        )
        if db_address is None:
            raise ValueError("Address not found")

        db_address.street = address.street
        db_address.zip_code = address.zip_code
        db_address.city = address.city
        db_address.state = address.state
        db_address.country = address.country
        db_address.client_id = address.client_id
        db_address.company_id = address.company_id

        self.db.commit()
        self.db.refresh(db_address)
        return db_address.to_domain()

    def delete(self, address_id: UUID) -> None:
        db_address = (
            self.db.query(AddressModel).filter(AddressModel.id == address_id).first()
        )
        if db_address is None:
            raise ValueError("Address not found")
        self.db.delete(db_address)
        self.db.commit()
