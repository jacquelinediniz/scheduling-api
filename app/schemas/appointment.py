import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class AppointmentCreate(BaseModel):
    service_id: uuid.UUID
    staff_id: uuid.UUID
    client_name: str = Field(..., min_length=2, max_length=255, examples=["João Silva"])
    client_email: EmailStr = Field(..., examples=["joao@email.com"])
    client_phone: str | None = Field(None, examples=["+55 11 99999-9999"])
    scheduled_at: datetime = Field(..., examples=["2026-06-01T10:00:00"])
    notes: str | None = None


class AppointmentResponse(BaseModel):
    id: uuid.UUID
    tenant_id: uuid.UUID
    service_id: uuid.UUID
    staff_id: uuid.UUID
    client_name: str
    client_email: str
    client_phone: str | None
    scheduled_at: datetime
    ends_at: datetime
    status: str
    notes: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class AppointmentUpdate(BaseModel):
    status: str | None = Field(None, examples=["confirmed", "cancelled", "completed"])
    notes: str | None = None
