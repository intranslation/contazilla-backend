import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from domain.entities.client import Client as ClientDomain
from shared.database import Base

if TYPE_CHECKING:
    from infrastructure.models.address import Address
    from infrastructure.models.user import User


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name = mapped_column(String, unique=False, nullable=False)
    cpf = mapped_column(String, unique=True, nullable=True)
    email = mapped_column(String, unique=True, nullable=True)
    phone = mapped_column(String, unique=False, nullable=True)
    is_premium = mapped_column(
        Boolean, default=False, server_default="false", nullable=False
    )

    created_at = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="clients")

    address: Mapped[Optional["Address"]] = relationship(
        back_populates="client", uselist=False, cascade="all, delete-orphan"
    )

    def to_domain(self):
        return ClientDomain(
            id=self.id,
            name=self.name,
            cpf=self.cpf,
            email=self.email,
            phone=self.phone,
            user_id=self.user_id,
            address=self.address.to_domain() if self.address else None,
            is_premium=self.is_premium,
        )
