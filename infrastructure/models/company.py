import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from domain.entities.company import Company as CompanyDomain
from shared.database import Base

if TYPE_CHECKING:
    from infrastructure.models.address import Address
    from infrastructure.models.user import User


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name = mapped_column(String, unique=False, nullable=False)
    cnpj = mapped_column(String, unique=True, nullable=False)
    created_at = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    client_id = mapped_column(UUID(as_uuid=True), nullable=True)

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="companies")

    address: Mapped[Optional["Address"]] = relationship(
        back_populates="company", uselist=False, cascade="all, delete-orphan"
    )

    def to_domain(self):
        return CompanyDomain(
            id=self.id,
            name=self.name,
            cnpj=self.cnpj,
            client_id=self.client_id,
            user_id=self.user_id,
            address=self.address.to_domain() if self.address else None,
        )
