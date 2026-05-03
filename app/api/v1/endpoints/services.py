import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.endpoints.auth import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.service import ServiceCreate, ServiceResponse, ServiceUpdate
from app.services.service_service import service_service

router = APIRouter(prefix="/services", tags=["services"])


@router.post("/", response_model=ServiceResponse, status_code=201)
async def create_service(
    data: ServiceCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Cria um novo serviço. Apenas admins podem criar serviços."""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can create services")
    return await service_service.create(db, current_user.tenant_id, data)


@router.get("/", response_model=list[ServiceResponse])
async def list_services(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Lista todos os serviços do tenant."""
    return await service_service.list_by_tenant(db, current_user.tenant_id)


@router.get("/{service_id}", response_model=ServiceResponse)
async def get_service(
    service_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Busca um serviço pelo ID."""
    service = await service_service.get_by_id(db, service_id, current_user.tenant_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service


@router.patch("/{service_id}", response_model=ServiceResponse)
async def update_service(
    service_id: uuid.UUID,
    data: ServiceUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Atualiza um serviço. Apenas admins."""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can update services")
    service = await service_service.get_by_id(db, service_id, current_user.tenant_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return await service_service.update(db, service, data)
