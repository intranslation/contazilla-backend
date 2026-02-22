import uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID

from shared.database import Base

from domain.entities import User as UserDomain


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, unique=False, index=False, nullable=False)
    phone = Column(String, unique=False, index=False, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def to_domain(self):
        return UserDomain(
            email=self.email,
            name=self.name,
            phone=self.phone,
            password=self.hashed_password,
        )
