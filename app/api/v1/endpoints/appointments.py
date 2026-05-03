import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.endpoints.auth import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.appointment import (
    AppointmentCreate,
    AppointmentResponse,
    AppointmentUpdate,
)
from app.services.appointment_service import appointment_service

router = APIRouter(prefix="/appointments", tags=["appointments"])


@router.post("/", response_model=AppointmentResponse, status_code=201)
async def create_appointment(
    data: AppointmentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Cria um novo agendamento.
    Valida automaticamente conflito de horário para o profissional.
    O horário de término é calculado automaticamente pela duração do serviço.
    """
    try:
        appointment = await appointment_service.create(db, current_user.tenant_id, data)
        return appointment
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[AppointmentResponse])
async def list_appointments(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Lista todos os agendamentos do tenant ordenados por data."""
    return await appointment_service.list_by_tenant(db, current_user.tenant_id)


@router.get("/{appointment_id}", response_model=AppointmentResponse)
async def get_appointment(
    appointment_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Busca um agendamento pelo ID."""
    appointment = await appointment_service.get_by_id(
        db, appointment_id, current_user.tenant_id
    )
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment


@router.patch("/{appointment_id}", response_model=AppointmentResponse)
async def update_appointment(
    appointment_id: uuid.UUID,
    data: AppointmentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Atualiza status ou notas de um agendamento.
    Status possíveis: pending, confirmed, cancelled, completed.
    """
    appointment = await appointment_service.get_by_id(
        db, appointment_id, current_user.tenant_id
    )
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return await appointment_service.update(db, appointment, data)
