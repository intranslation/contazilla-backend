import uuid
from typing import TYPE_CHECKING

from sqlalchemy import (UUID, Boolean, Column, DateTime, Float, ForeignKey,
                        String)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from domain.entities.asset import Asset as AssetDomain
from shared.database import Base

if TYPE_CHECKING:
    from infrastructure.models.user import User


class Asset(Base):
    __tablename__ = "assets"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    filename = Column(String, unique=False, nullable=True)
    size = Column(Float, nullable=True)
    was_viewed = Column(Boolean, nullable=False, server_default="false")
    was_downloaded = Column(Boolean, nullable=False, server_default="false")
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
    user: Mapped["User"] = relationship(back_populates="assets")

    def to_domain(self):
        return AssetDomain(
            id=self.id,
            filename=self.filename,
            client_id=self.client_id,
            user_id=self.user_id,
            size=self.size,
            was_viewed=self.was_viewed,
            was_downloaded=self.was_downloaded,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
