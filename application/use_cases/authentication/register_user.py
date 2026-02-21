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
            raise

        hashed_password: str = hash_service.get_password_hash(password)
        new_user = User(
            email=email, name=name, phone=phone, hashed_password=hashed_password
        )

        auth_repo.create_user(new_user)

        return new_user
