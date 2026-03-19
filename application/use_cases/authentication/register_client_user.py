from uuid import UUID

from application.ports import ClientRepository, PasswordHashing, UserRepository
from domain.entities.user import User
from domain.enums.role import UserRole


class RegisterClientUser:
    def __init__(
        self,
        user_repo: UserRepository,
        client_repo: ClientRepository,
        password_hashing: PasswordHashing,
    ) -> None:
        self.user_repo = user_repo
        self.client_repo = client_repo
        self.password_hashing = password_hashing

    def execute(self, client_id: UUID, user_id: UUID, temp_password: str):
        client = self.client_repo.get_by_id(client_id=client_id, user_id=user_id)

        if client is None:
            raise ValueError("Client not found")

        if not client.email:
            raise ValueError("Client must have an email to register a user")

        if self.user_repo.user_exists(email=client.email):
            raise ValueError("A user with this email already exists")

        hashed_password = self.password_hashing.get_password_hash(temp_password)

        new_user = User(
            id=None,
            email=client.email,
            name=client.name,
            phone=client.phone,
            password=hashed_password,
            role=UserRole.ADMIN,
        )

        self.user_repo.create_user(user=new_user)

        return new_user
