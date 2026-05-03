import uuid
from datetime import timedelta

from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.appointment import Appointment
from app.models.service import Service
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate


class AppointmentService:
    async def create(
        self,
        db: AsyncSession,
        tenant_id: uuid.UUID,
        data: AppointmentCreate,
    ) -> Appointment:
        # Busca o serviço para saber a duração
        service_result = await db.execute(
            select(Service).where(
                Service.id == data.service_id,
                Service.tenant_id == tenant_id,
            )
        )
        service = service_result.scalar_one_or_none()
        if not service:
            raise ValueError("Service not found")

        # Calcula o horário de término baseado na duração do serviço
        ends_at = data.scheduled_at + timedelta(minutes=service.duration_minutes)

        # Verifica conflito de horário para o mesmo profissional
        conflict = await db.execute(
            select(Appointment).where(
                and_(
                    Appointment.staff_id == data.staff_id,
                    Appointment.tenant_id == tenant_id,
                    Appointment.status.notin_(["cancelled"]),
                    or_(
                        # Novo agendamento começa durante um existente
                        and_(
                            Appointment.scheduled_at <= data.scheduled_at,
                            Appointment.ends_at > data.scheduled_at,
                        ),
                        # Novo agendamento termina durante um existente
                        and_(
                            Appointment.scheduled_at < ends_at,
                            Appointment.ends_at >= ends_at,
                        ),
                        # Novo agendamento engloba um existente
                        and_(
                            Appointment.scheduled_at >= data.scheduled_at,
                            Appointment.ends_at <= ends_at,
                        ),
                    ),
                )
            )
        )
        if conflict.scalar_one_or_none():
            raise ValueError(
                "Time slot not available — professional already has an appointment"
            )

        appointment = Appointment(
            tenant_id=tenant_id,
            service_id=data.service_id,
            staff_id=data.staff_id,
            client_name=data.client_name,
            client_email=data.client_email,
            client_phone=data.client_phone,
            scheduled_at=data.scheduled_at,
            ends_at=ends_at,
            notes=data.notes,
        )
        db.add(appointment)
        await db.flush()
        await db.refresh(appointment)
        return appointment

    async def get_by_id(
        self,
        db: AsyncSession,
        appointment_id: uuid.UUID,
        tenant_id: uuid.UUID,
    ) -> Appointment | None:
        result = await db.execute(
            select(Appointment).where(
                Appointment.id == appointment_id,
                Appointment.tenant_id == tenant_id,
            )
        )
        return result.scalar_one_or_none()

    async def list_by_tenant(
        self,
        db: AsyncSession,
        tenant_id: uuid.UUID,
    ) -> list[Appointment]:
        result = await db.execute(
            select(Appointment)
            .where(Appointment.tenant_id == tenant_id)
            .order_by(Appointment.scheduled_at)
        )
        return list(result.scalars().all())

    async def update(
        self,
        db: AsyncSession,
        appointment: Appointment,
        data: AppointmentUpdate,
    ) -> Appointment:
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(appointment, field, value)
        await db.flush()
        await db.refresh(appointment)
        return appointment


appointment_service = AppointmentService()
