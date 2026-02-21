from sqlalchemy.orm import Session
from domain.entities.user import User
from infrastructure.models.user import User as UserModel


class AuthenticationRepository:
    def __init__(self, db: Session) -> None:
        self.db: Session = db

    def create_user(self, user: User) -> None:
        self.db.add(user)
        self.db.commit()

    def user_exists(self, email: str) -> bool:
        user_exists = self.db.query(UserModel).filter(UserModel.email == email).first()
        return user_exists is not None

    def get_user(self, email: str) -> User | None:
        user = self.db.query(UserModel).filter(UserModel.email == email).first()
        return user
