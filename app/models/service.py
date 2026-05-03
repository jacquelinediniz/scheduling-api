from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base

if TYPE_CHECKING:
    from app.models.tenant import Tenant
    from app.models.appointment import Appointment


class Service(Base):
    """
    Representa um serviço oferecido por um tenant.
    Ex: Corte de cabelo (30min, R$50), Consulta médica (60min, R$200).
    """

    __tablename__ = "services"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )  # preço em centavos ex: R$50,00 = 5000
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relacionamentos
    tenant: Mapped[Tenant] = relationship("Tenant", back_populates="services")
    appointments: Mapped[list[Appointment]] = relationship(
        "Appointment", back_populates="service"
    )

    def __repr__(self) -> str:
        return f"<Service {self.name} ({self.duration_minutes}min)>"
