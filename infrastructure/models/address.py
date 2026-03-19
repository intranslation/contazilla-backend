import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import UUID, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain.entities.address import Address as AddressDomain
from shared.database import Base

if TYPE_CHECKING:
    from infrastructure.models.client import Client
    from infrastructure.models.company import Company


class Address(Base):
    __tablename__ = "addresses"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    street = mapped_column(String, unique=False, nullable=True)
    zip_code = mapped_column(String, unique=False, nullable=True)
    city = mapped_column(String, unique=False, nullable=True)
    state = mapped_column(String, unique=False, nullable=True)
    country = mapped_column(String, unique=False, nullable=True)

    client_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("clients.id"), nullable=True
    )
    client: Mapped[Optional["Client"]] = relationship(back_populates="address")

    company_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("companies.id"), nullable=True
    )
    company: Mapped[Optional["Company"]] = relationship(back_populates="address")

    def to_domain(self):
        return AddressDomain(
            id=self.id,
            street=self.street,
            zip_code=self.zip_code,
            city=self.city,
            state=self.state,
            country=self.country,
            client_id=self.client_id,
            company_id=self.company_id,
        )
