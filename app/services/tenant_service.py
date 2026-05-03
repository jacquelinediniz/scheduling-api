import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tenant import Tenant
from app.schemas.tenant import TenantCreate, TenantUpdate


class TenantService:
    """
    Contém toda a lógica de negócio relacionada a Tenants.
    Os endpoints chamam os métodos deste service — nunca acessam
    o banco diretamente.
    """

    async def create(self, db: AsyncSession, data: TenantCreate) -> Tenant:
        """Cria um novo tenant verificando se o slug já existe."""
        existing = await db.execute(select(Tenant).where(Tenant.slug == data.slug))
        if existing.scalar_one_or_none():
            raise ValueError(f"Slug '{data.slug}' already in use")

        tenant = Tenant(
            name=data.name,
            slug=data.slug,
            email=data.email,
        )
        db.add(tenant)
        await db.flush()  # envia para o banco mas não commita ainda
        await db.refresh(tenant)  # recarrega o objeto com os dados do banco
        return tenant

    async def get_by_id(self, db: AsyncSession, tenant_id: uuid.UUID) -> Tenant | None:
        """Busca um tenant pelo ID."""
        result = await db.execute(select(Tenant).where(Tenant.id == tenant_id))
        return result.scalar_one_or_none()

    async def get_by_slug(self, db: AsyncSession, slug: str) -> Tenant | None:
        """Busca um tenant pelo slug."""
        result = await db.execute(select(Tenant).where(Tenant.slug == slug))
        return result.scalar_one_or_none()

    async def list_all(self, db: AsyncSession) -> list[Tenant]:
        """Lista todos os tenants ativos."""
        result = await db.execute(
            select(Tenant).where(Tenant.is_active).order_by(Tenant.name)
        )
        return list(result.scalars().all())

    async def update(
        self,
        db: AsyncSession,
        tenant: Tenant,
        data: TenantUpdate,
    ) -> Tenant:
        """Atualiza apenas os campos enviados."""
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(tenant, field, value)
        await db.flush()
        await db.refresh(tenant)
        return tenant

    async def delete(self, db: AsyncSession, tenant: Tenant) -> None:
        """Desativa o tenant em vez de deletar — soft delete."""
        tenant.is_active = False
        await db.flush()


tenant_service = TenantService()
