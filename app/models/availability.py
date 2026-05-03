from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Integer, Time
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base

if TYPE_CHECKING:
    from app.models.user import User


class Availability(Base):
    """
    Define os horários disponíveis de um profissional.
    Ex: Dra. Ana disponível Segunda a Sexta das 8h às 18h.

    weekday: 0=Segunda, 1=Terça, 2=Quarta, 3=Quinta, 4=Sexta, 5=Sábado, 6=Domingo
    """

    __tablename__ = "availabilities"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
    )
    weekday: Mapped[int] = mapped_column(Integer, nullable=False)  # 0-6
    start_time: Mapped[str] = mapped_column(Time, nullable=False)  # ex: 08:00
    end_time: Mapped[str] = mapped_column(Time, nullable=False)  # ex: 18:00
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relacionamento
    user: Mapped[User] = relationship("User", back_populates="availabilities")

    def __repr__(self) -> str:
        return (
            f"<Availability weekday={self.weekday} {self.start_time}-{self.end_time}>"
        )
