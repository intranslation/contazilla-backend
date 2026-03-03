from fastapi import HTTPException
from application.ports import UserRepository, PasswordHashing
from domain.entities.user import User


class RegisterUser:
    def __init__(
        self, user_repo: UserRepository, password_hashing: PasswordHashing
    ) -> None:
        self.user_repo = user_repo
        self.password_hashing = password_hashing

    def execute(
        self,
        email: str,
        name: str,
        phone: str,
        password: str,
    ):
        user_exists: bool = self.user_repo.user_exists(email)

        if user_exists:
            raise ValueError("An user already exists with this email")

        hashed_password: str = self.password_hashing.get_password_hash(password)
        new_user = User(
            id=None, email=email, name=name, phone=phone, password=hashed_password
        )

        try:
            self.user_repo.create_user(new_user)
        except Exception as e:
            print(str(e))
            raise ValueError("Error while creating a new account.")

        return new_user
