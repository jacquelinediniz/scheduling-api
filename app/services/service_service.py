import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.service import Service
from app.schemas.service import ServiceCreate, ServiceUpdate


class ServiceService:
    async def create(
        self, db: AsyncSession, tenant_id: uuid.UUID, data: ServiceCreate
    ) -> Service:
        service = Service(
            tenant_id=tenant_id,
            name=data.name,
            description=data.description,
            duration_minutes=data.duration_minutes,
            price=data.price,
        )
        db.add(service)
        await db.flush()
        await db.refresh(service)
        return service

    async def get_by_id(
        self, db: AsyncSession, service_id: uuid.UUID, tenant_id: uuid.UUID
    ) -> Service | None:
        result = await db.execute(
            select(Service).where(
                Service.id == service_id, Service.tenant_id == tenant_id
            )
        )
        return result.scalar_one_or_none()

    async def list_by_tenant(
        self, db: AsyncSession, tenant_id: uuid.UUID
    ) -> list[Service]:
        result = await db.execute(
            select(Service)
            .where(Service.tenant_id == tenant_id, Service.is_active)
            .order_by(Service.name)
        )
        return list(result.scalars().all())

    async def update(
        self, db: AsyncSession, service: Service, data: ServiceUpdate
    ) -> Service:
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(service, field, value)
        await db.flush()
        await db.refresh(service)
        return service


service_service = ServiceService()
