import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password, verify_password
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    """Contém toda a lógica de negócio relacionada a Users."""

    async def create(
        self,
        db: AsyncSession,
        tenant_id: uuid.UUID,
        data: UserCreate,
    ) -> User:
        """Cria um usuário dentro de um tenant."""
        existing = await db.execute(
            select(User).where(
                User.email == data.email,
                User.tenant_id == tenant_id,
            )
        )
        if existing.scalar_one_or_none():
            raise ValueError(f"Email '{data.email}' already in use in this tenant")

        user = User(
            tenant_id=tenant_id,
            name=data.name,
            email=data.email,
            hashed_password=hash_password(data.password),
            role=data.role,
        )
        db.add(user)
        await db.flush()
        await db.refresh(user)
        return user

    async def get_by_id(
        self,
        db: AsyncSession,
        user_id: uuid.UUID,
        tenant_id: uuid.UUID,
    ) -> User | None:
        """Busca usuário por ID dentro do tenant correto."""
        result = await db.execute(
            select(User).where(
                User.id == user_id,
                User.tenant_id == tenant_id,
            )
        )
        return result.scalar_one_or_none()

    async def get_by_email(
        self,
        db: AsyncSession,
        email: str,
        tenant_id: uuid.UUID,
    ) -> User | None:
        """Busca usuário por email dentro do tenant."""
        result = await db.execute(
            select(User).where(
                User.email == email,
                User.tenant_id == tenant_id,
            )
        )
        return result.scalar_one_or_none()

    async def list_by_tenant(
        self,
        db: AsyncSession,
        tenant_id: uuid.UUID,
    ) -> list[User]:
        """Lista todos os usuários de um tenant."""
        result = await db.execute(
            select(User)
            .where(User.tenant_id == tenant_id, User.is_active)
            .order_by(User.name)
        )
        return list(result.scalars().all())

    async def authenticate(
        self,
        db: AsyncSession,
        email: str,
        password: str,
        tenant_id: uuid.UUID,
    ) -> User | None:
        """
        Verifica email e senha — usado no login.
        Retorna o usuário se as credenciais estiverem corretas, None caso contrário.
        """
        user = await self.get_by_email(db, email, tenant_id)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    async def update(
        self,
        db: AsyncSession,
        user: User,
        data: UserUpdate,
    ) -> User:
        """Atualiza apenas os campos enviados."""
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        await db.flush()
        await db.refresh(user)
        return user


user_service = UserService()
