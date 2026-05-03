import uuid
from datetime import time

from pydantic import BaseModel, Field, model_validator


class AvailabilityCreate(BaseModel):
    user_id: uuid.UUID
    weekday: int = Field(..., ge=0, le=6, examples=[0])  # 0=Segunda
    start_time: time = Field(..., examples=["08:00:00"])
    end_time: time = Field(..., examples=["18:00:00"])

    @model_validator(mode="after")
    def end_must_be_after_start(self) -> "AvailabilityCreate":
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be after start_time")
        return self


class AvailabilityResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    tenant_id: uuid.UUID
    weekday: int
    start_time: time
    end_time: time
    is_active: bool

    model_config = {"from_attributes": True}
