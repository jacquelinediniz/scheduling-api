import pytest

from tests.factories import TenantFactory


@pytest.mark.asyncio
async def test_create_tenant(client):
    """Verifica que um tenant pode ser criado com dados válidos."""
    data = TenantFactory.build()
    response = await client.post("/api/v1/tenants/", json=data)
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == data["name"]
    assert body["slug"] == data["slug"]
    assert body["email"] == data["email"]
    assert body["is_active"] is True


@pytest.mark.asyncio
async def test_create_tenant_duplicate_slug(client):
    """Verifica que não é possível criar dois tenants com o mesmo slug."""
    data = TenantFactory.build(slug="slug-unico")
    await client.post("/api/v1/tenants/", json=data)

    # Tenta criar outro com o mesmo slug
    data2 = TenantFactory.build(slug="slug-unico")
    response = await client.post("/api/v1/tenants/", json=data2)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_list_tenants(client):
    """Verifica que a listagem de tenants funciona."""
    # Cria 2 tenants
    await client.post("/api/v1/tenants/", json=TenantFactory.build())
    await client.post("/api/v1/tenants/", json=TenantFactory.build())

    response = await client.get("/api/v1/tenants/")
    assert response.status_code == 200
    assert len(response.json()) >= 2


@pytest.mark.asyncio
async def test_get_tenant_by_id(client):
    """Verifica que um tenant pode ser buscado pelo ID."""
    data = TenantFactory.build()
    create_response = await client.post("/api/v1/tenants/", json=data)
    tenant_id = create_response.json()["id"]

    response = await client.get(f"/api/v1/tenants/{tenant_id}")
    assert response.status_code == 200
    assert response.json()["id"] == tenant_id


@pytest.mark.asyncio
async def test_get_tenant_not_found(client):
    """Verifica que buscar um tenant inexistente retorna 404."""
    response = await client.get("/api/v1/tenants/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_tenant(client):
    """Verifica que um tenant pode ser atualizado."""
    data = TenantFactory.build()
    create_response = await client.post("/api/v1/tenants/", json=data)
    tenant_id = create_response.json()["id"]

    response = await client.patch(
        f"/api/v1/tenants/{tenant_id}",
        json={"name": "Nome Atualizado"},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Nome Atualizado"
