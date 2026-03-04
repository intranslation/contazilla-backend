import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from shared.database import Base

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.sql import func
from sqlalchemy import Column, String, DateTime, ForeignKey

from domain.entities.client import Client as ClientDomain

User = None


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name = Column(String, unique=False, nullable=True)
    cpf = Column(String, unique=True, nullable=False)
    phone = Column(String, unique=False, nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="clients")

    def to_domain(self):
        return ClientDomain(
            id=self.id,
            name=self.name,
            cpf=self.cpf,
            phone=self.phone,
            user_id=self.user_id,
        )
