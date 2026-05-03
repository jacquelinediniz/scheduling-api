import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """Schema para criar um novo usuário dentro de um tenant."""

    name: str = Field(..., min_length=2, max_length=255, examples=["João Silva"])
    email: EmailStr = Field(..., examples=["joao@email.com"])
    password: str = Field(..., min_length=8, examples=["senha123"])
    role: str = Field(default="client", examples=["admin", "staff", "client"])


class UserResponse(BaseModel):
    """
    Schema para retornar dados de um usuário.
    Note que hashed_password NUNCA aparece aqui — segurança.
    """

    id: uuid.UUID
    tenant_id: uuid.UUID
    name: str
    email: str
    role: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    """Schema para atualizar um usuário."""

    name: str | None = Field(None, min_length=2, max_length=255)
    email: EmailStr | None = None
    role: str | None = None
    is_active: bool | None = None


class Token(BaseModel):
    """Schema do token JWT retornado no login."""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Dados extraídos do token JWT após validação."""

    user_id: uuid.UUID | None = None
    tenant_id: uuid.UUID | None = None
    role: str | None = None
