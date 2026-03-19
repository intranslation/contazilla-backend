import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from domain.entities import User as UserDomain
from shared.database import Base

if TYPE_CHECKING:
    from infrastructure.models.asset import Asset
    from infrastructure.models.client import Client
    from infrastructure.models.company import Company


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    email = mapped_column(String, unique=True, index=True, nullable=False)
    name = mapped_column(String, unique=False, index=False, nullable=False)
    phone = mapped_column(String, unique=False, index=False, nullable=False)
    hashed_password = mapped_column(String, nullable=False)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    role = mapped_column(String, nullable=False, default="admin")
    is_archived = mapped_column(Boolean, nullable=True, default=False)

    assets: Mapped[list["Asset"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    clients: Mapped[list["Client"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    companies: Mapped[list["Company"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def to_domain(self):
        return UserDomain(
            id=self.id,
            email=self.email,
            name=self.name,
            phone=self.phone,
            password=self.hashed_password,
            role=self.role,
            is_archived=self.is_archived,
        )
