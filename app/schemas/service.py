import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class ServiceCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=255, examples=["Consulta Médica"])
    description: str | None = Field(None, examples=["Consulta de rotina"])
    duration_minutes: int = Field(..., gt=0, le=480, examples=[60])
    price: int = Field(..., ge=0, examples=[20000])  # em centavos


class ServiceResponse(BaseModel):
    id: uuid.UUID
    tenant_id: uuid.UUID
    name: str
    description: str | None
    duration_minutes: int
    price: int
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class ServiceUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=255)
    description: str | None = None
    duration_minutes: int | None = Field(None, gt=0, le=480)
    price: int | None = Field(None, ge=0)
    is_active: bool | None = None
