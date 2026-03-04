import uuid
from sqlalchemy.orm import mapped_column, relationship, Mapped
from shared.database import Base

from sqlalchemy.sql import func
from sqlalchemy import Column, String, DateTime, UUID, ForeignKey

from domain.entities.asset import Asset as AssetDomain

User = None


class Asset(Base):
    __tablename__ = "assets"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
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
    user: Mapped["User"] = relationship(back_populates="assets")

    def to_domain(self):
        return AssetDomain(
            id=self.id,
            filename=self.filename,
            url=self.url,
            client_id=self.client_id,
            user_id=self.user_id,
        )
