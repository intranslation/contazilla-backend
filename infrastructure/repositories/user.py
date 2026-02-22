from sqlalchemy.orm import Session
from domain.entities.user import User
from infrastructure.models.user import User as UserModel


class UserRepository:
    def __init__(self, db: Session) -> None:
        self.db: Session = db

    def create_user(self, user: User) -> None:
        new_user = UserModel(
            email=user.email,
            name=user.name,
            phone=user.phone,
            hashed_password=user.password,
        )
        self.db.add(new_user)
        self.db.commit()

    def user_exists(self, email: str) -> bool:
        user_exists = self.db.query(UserModel).filter(UserModel.email == email).first()
        return user_exists is not None

    def get_user_by_email(self, email: str) -> UserModel | None:
        user = self.db.query(UserModel).filter(UserModel.email == email).first()

        if user is None:
            raise BaseException()

        return user.to_domain()
