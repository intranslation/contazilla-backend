from uuid import UUID

from sqlalchemy.orm import Session

from application.ports import ClientRepository as ClientRepositoryContract
from domain.entities.client import Client
from infrastructure.models.client import Client as ClientModel


class ClientRepository(ClientRepositoryContract):
    def __init__(self, db: Session) -> None:
        self.db: Session = db

    def create(self, client: Client) -> Client:
        new_client = ClientModel(
            name=client.name,
            cpf=client.cpf,
            phone=client.phone,
            is_premium=client.is_premium,
            user_id=client.user_id,
        )
        self.db.add(new_client)
        self.db.commit()
        self.db.refresh(new_client)
        return new_client.to_domain()

    def get_by_id(self, client_id: UUID, user_id: UUID) -> Client | None:
        client = (
            self.db.query(ClientModel)
            .filter(ClientModel.id == client_id, ClientModel.user_id == user_id)
            .first()
        )
        if client is None:
            return None
        return client.to_domain()

    def list_by_user(self, user_id: UUID) -> list[Client]:
        clients = (
            self.db.query(ClientModel).filter(ClientModel.user_id == user_id).all()
        )
        return [c.to_domain() for c in clients]

    def update(self, client: Client) -> Client:
        db_client = (
            self.db.query(ClientModel)
            .filter(ClientModel.id == client.id, ClientModel.user_id == client.user_id)
            .first()
        )
        if db_client is None:
            raise ValueError("Client not found")

        db_client.name = client.name
        db_client.cpf = client.cpf
        db_client.email = client.email
        db_client.phone = client.phone
        db_client.is_premium = client.is_premium

        self.db.commit()

        return db_client.to_domain()

    def delete(self, client_id: UUID, user_id: UUID) -> None:
        db_client = (
            self.db.query(ClientModel)
            .filter(ClientModel.id == client_id, ClientModel.user_id == user_id)
            .first()
        )
        if db_client is None:
            raise ValueError("Client not found")
        self.db.delete(db_client)
        self.db.commit()
