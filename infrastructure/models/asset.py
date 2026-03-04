from sqlalchemy.orm import mapped_column, relationship, Mapped
from shared.database import Base

from sqlalchemy.sql import func
from sqlalchemy import Column, String, DateTime, UUID, ForeignKey


class Asset(Base):
    filename = Column(String, unique=False, nullable=True)
    url = Column(String, unique=True, nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    client_id = mapped_column(UUID(as_uuid=True), nullable=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="orders")
