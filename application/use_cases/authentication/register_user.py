from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from application.ports.repositories.authentication import AuthenticationRepository
from application.services import HashingUtilitiesService
from domain.entities.user import User


class RegisterUser:
    @staticmethod
    def execute(
        auth_repo: AuthenticationRepository,
        hash_service: HashingUtilitiesService,
        email: str,
        name: str,
        phone: str,
        password: str,
    ):
        user_exists: bool = auth_repo.user_exists(email)

        if user_exists:
            raise HTTPException(409, detail="User already exists with this e-mail")

        hashed_password: str = hash_service.get_password_hash(password)
        new_user = User(email=email, name=name, phone=phone, password=hashed_password)

        try:
            auth_repo.create_user(new_user)
        except:
            raise HTTPException(409, detail="Error while creating a new account.")

        return new_user
