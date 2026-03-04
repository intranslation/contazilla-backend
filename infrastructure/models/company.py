from sqlalchemy.orm.properties import MappedColumn
from typing import Any
import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from shared.database import Base
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.sql import func
from sqlalchemy import ForeignKey, String, DateTime

from domain.entities.company import Company as CompanyDomain

User = None


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: MappedColumn[String] = mapped_column(String, unique=False, nullable=False)
    address: MappedColumn[String] = mapped_column(String, unique=False, nullable=False)
    cnpj: MappedColumn[String] = mapped_column(String, unique=True, nullable=False)
    created_at: MappedColumn[Any] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: MappedColumn[Any] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    client_id = mapped_column(UUID(as_uuid=True), nullable=True)

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="companies")

    def to_domain(self):
        return CompanyDomain(
            id=self.id,
            name=self.name,
            address=self.address,
            cnpj=self.cnpj,
            client_id=self.client_id,
            user_id=self.user_id,
        )
