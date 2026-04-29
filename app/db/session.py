from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

# Motor de conexão assíncrono com o PostgreSQL
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,  # loga todas as queries SQL quando debug=True
)

# Fábrica de sessões — cada requisição vai criar uma sessão a partir daqui
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """
    Classe base para todos os modelos do banco.
    Todos os models vão herdar desta classe.
    """

    pass


async def get_db():
    """
    Dependency do FastAPI — fornece uma sessão do banco para cada requisição.
    O 'yield' garante que a sessão é fechada após a requisição terminar,
    mesmo se ocorrer um erro.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
