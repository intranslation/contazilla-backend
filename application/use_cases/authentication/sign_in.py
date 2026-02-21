from datetime import timedelta
from fastapi import HTTPException, status
from application.ports.repositories.authentication import AuthenticationRepository
from application.services.hashing_utilities import HashingUtilitiesService

from shared.config import settings


class SignIn:
    @staticmethod
    def execute(
        auth_repo: AuthenticationRepository,
        hash_service: HashingUtilitiesService,
        email: str,
        password: str,
    ):
        user = auth_repo.get_user(email=email)

        if not user or not hash_service.verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = hash_service.create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )

        return {"access_token": access_token, "token_type": "bearer"}
