import pytest

from tests.factories import TenantFactory, UserFactory


async def create_tenant_and_user(client):
    """Helper — cria tenant e usuário para reusar nos testes."""
    tenant_data = TenantFactory.build()
    tenant_response = await client.post("/api/v1/tenants/", json=tenant_data)
    slug = tenant_response.json()["slug"]

    user_data = UserFactory.build()
    user_response = await client.post(
        f"/api/v1/auth/register?tenant_slug={slug}",
        json=user_data,
    )
    return slug, user_data, user_response.json()


@pytest.mark.asyncio
async def test_register_user(client):
    """Verifica que um usuário pode ser registrado."""
    tenant_data = TenantFactory.build()
    await client.post("/api/v1/tenants/", json=tenant_data)

    user_data = UserFactory.build()
    response = await client.post(
        f"/api/v1/auth/register?tenant_slug={tenant_data['slug']}",
        json=user_data,
    )
    assert response.status_code == 201
    body = response.json()
    assert body["email"] == user_data["email"]
    assert "hashed_password" not in body  # senha nunca exposta


@pytest.mark.asyncio
async def test_login_success(client):
    """Verifica que o login retorna um token JWT válido."""
    slug, user_data, _ = await create_tenant_and_user(client)

    response = await client.post(
        f"/api/v1/auth/login?tenant_slug={slug}",
        data={
            "username": user_data["email"],
            "password": user_data["password"],
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(client):
    """Verifica que login com senha errada retorna 401."""
    slug, user_data, _ = await create_tenant_and_user(client)

    response = await client.post(
        f"/api/v1/auth/login?tenant_slug={slug}",
        data={
            "username": user_data["email"],
            "password": "senha_errada",
        },
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_me(client):
    """Verifica que o endpoint /me retorna dados do usuário logado."""
    slug, user_data, _ = await create_tenant_and_user(client)

    login_response = await client.post(
        f"/api/v1/auth/login?tenant_slug={slug}",
        data={
            "username": user_data["email"],
            "password": user_data["password"],
        },
    )
    token = login_response.json()["access_token"]

    response = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["email"] == user_data["email"]


@pytest.mark.asyncio
async def test_get_me_without_token(client):
    """Verifica que /me sem token retorna 401."""
    response = await client.get("/api/v1/auth/me")
    assert response.status_code == 401
