import pytest

from tests.factories import ServiceFactory, TenantFactory, UserFactory


async def setup_appointment_data(client):
    """Helper — cria tudo necessário para testar agendamentos."""
    # Cria tenant
    tenant_data = TenantFactory.build()
    await client.post("/api/v1/tenants/", json=tenant_data)
    slug = tenant_data["slug"]

    # Cria usuário admin
    user_data = UserFactory.build(role="admin")
    user_response = await client.post(
        f"/api/v1/auth/register?tenant_slug={slug}",
        json=user_data,
    )
    staff_id = user_response.json()["id"]

    # Faz login
    login_response = await client.post(
        f"/api/v1/auth/login?tenant_slug={slug}",
        data={
            "username": user_data["email"],
            "password": user_data["password"],
        },
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Cria serviço
    service_response = await client.post(
        "/api/v1/services/",
        json=ServiceFactory.build(),
        headers=headers,
    )
    service_id = service_response.json()["id"]

    return headers, service_id, staff_id


@pytest.mark.asyncio
async def test_create_appointment(client):
    """Verifica que um agendamento pode ser criado."""
    headers, service_id, staff_id = await setup_appointment_data(client)

    response = await client.post(
        "/api/v1/appointments/",
        json={
            "service_id": service_id,
            "staff_id": staff_id,
            "client_name": "João Silva",
            "client_email": "joao@email.com",
            "scheduled_at": "2026-07-01T10:00:00",
        },
        headers=headers,
    )
    assert response.status_code == 201
    body = response.json()
    assert body["client_name"] == "João Silva"
    assert body["status"] == "pending"
    assert body["ends_at"] is not None


@pytest.mark.asyncio
async def test_appointment_conflict(client):
    """Verifica que conflito de horário retorna erro 400."""
    headers, service_id, staff_id = await setup_appointment_data(client)

    appointment_data = {
        "service_id": service_id,
        "staff_id": staff_id,
        "client_name": "João Silva",
        "client_email": "joao@email.com",
        "scheduled_at": "2026-07-01T14:00:00",
    }

    # Primeiro agendamento — deve funcionar
    response1 = await client.post(
        "/api/v1/appointments/",
        json=appointment_data,
        headers=headers,
    )
    assert response1.status_code == 201

    # Segundo agendamento no mesmo horário — deve falhar
    appointment_data["client_name"] = "Maria Santos"
    appointment_data["client_email"] = "maria@email.com"
    response2 = await client.post(
        "/api/v1/appointments/",
        json=appointment_data,
        headers=headers,
    )
    assert response2.status_code == 400
    assert "Time slot not available" in response2.json()["detail"]


@pytest.mark.asyncio
async def test_list_appointments(client):
    """Verifica que a listagem de agendamentos funciona."""
    headers, service_id, staff_id = await setup_appointment_data(client)

    await client.post(
        "/api/v1/appointments/",
        json={
            "service_id": service_id,
            "staff_id": staff_id,
            "client_name": "Cliente 1",
            "client_email": "cliente1@email.com",
            "scheduled_at": "2026-07-02T10:00:00",
        },
        headers=headers,
    )

    response = await client.get("/api/v1/appointments/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) >= 1
