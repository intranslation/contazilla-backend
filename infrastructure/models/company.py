from sqlalchemy.orm.properties import MappedColumn
from typing import Any
import uuid
from sqlalchemy.orm import Mapped, mapped_column
from shared.database import Base
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.sql import func
from sqlalchemy import String, DateTime


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
