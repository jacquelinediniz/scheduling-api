import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator


class TenantCreate(BaseModel):
    """
    Schema para criar um novo tenant.
    Estes são os dados que o cliente envia no body da requisição.
    """

    name: str = Field(..., min_length=2, max_length=255, examples=["Clínica Dra. Ana"])
    slug: str = Field(
        ...,
        min_length=2,
        max_length=100,
        pattern=r"^[a-z0-9-]+$",
        examples=["clinica-dra-ana"],
    )
    email: EmailStr = Field(..., examples=["contato@clinicadrana.com.br"])

    @field_validator("slug")
    @classmethod
    def slug_must_be_lowercase(cls, v: str) -> str:
        """Garante que o slug é sempre minúsculo."""
        return v.lower()


class TenantResponse(BaseModel):
    """
    Schema para retornar dados de um tenant.
    Estes são os dados que a API devolve ao cliente.
    Note que não incluímos campos sensíveis aqui.
    """

    id: uuid.UUID
    name: str
    slug: str
    email: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}
    # from_attributes=True permite converter um objeto SQLAlchemy
    # diretamente em schema Pydantic


class TenantUpdate(BaseModel):
    """
    Schema para atualizar um tenant.
    Todos os campos são opcionais — o cliente envia só o que quer mudar.
    """

    name: str | None = Field(None, min_length=2, max_length=255)
    email: EmailStr | None = None
    is_active: bool | None = None
