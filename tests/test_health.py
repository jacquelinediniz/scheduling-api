import pytest


@pytest.mark.asyncio
async def test_health_check(client):
    """Verifica que o endpoint de health check retorna 200."""
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "version": "0.1.0"}
