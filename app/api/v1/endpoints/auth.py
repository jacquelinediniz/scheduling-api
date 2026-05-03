import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, decode_access_token
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import Token, UserCreate, UserResponse
from app.services.tenant_service import tenant_service
from app.services.user_service import user_service

router = APIRouter(prefix="/auth", tags=["auth"])

# Esquema OAuth2 — diz ao FastAPI onde encontrar o token nas requisições
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Dependency que extrai e valida o usuário do token JWT.
    Usada para proteger endpoints — qualquer rota que usar esta
    dependency exige autenticação.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    user_id = payload.get("sub")
    tenant_id = payload.get("tenant_id")

    if not user_id or not tenant_id:
        raise credentials_exception

    user = await user_service.get_by_id(
        db,
        uuid.UUID(user_id),
        uuid.UUID(tenant_id),
    )
    if not user:
        raise credentials_exception
    return user


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(
    tenant_slug: str,
    data: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Registra um novo usuário em um tenant existente.
    O tenant_slug identifica em qual empresa o usuário será criado.
    """
    tenant = await tenant_service.get_by_slug(db, tenant_slug)
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found",
        )
    try:
        user = await user_service.create(db, tenant.id, data)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/login", response_model=Token)
async def login(
    tenant_slug: str,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """
    Realiza o login e retorna um token JWT.
    O token deve ser enviado no header Authorization: Bearer <token>
    em todas as requisições autenticadas.
    """
    tenant = await tenant_service.get_by_slug(db, tenant_slug)
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found",
        )

    user = await user_service.authenticate(
        db,
        form_data.username,
        form_data.password,
        tenant.id,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": str(user.id), "tenant_id": str(user.tenant_id), "role": user.role}
    )
    return Token(access_token=access_token)


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """
    Retorna os dados do usuário autenticado.
    Endpoint protegido — exige token JWT válido.
    """
    return current_user
