import uuid
from sqlalchemy.orm import Mapped, mapped_column
from shared.database import Base

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.sql import func
from sqlalchemy import Column, String, DateTime


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
