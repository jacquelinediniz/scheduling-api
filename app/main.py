from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.api.v1.endpoints import auth, tenants


app = FastAPI(
    title="Scheduling API",
    description="Multi-tenant scheduling API for businesses",
    version="0.1.0",
)

# Registra os routers com o prefixo /api/v1
app.include_router(tenants.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Scheduling API",
        version="0.1.0",
        description="Multi-tenant scheduling API for businesses",
        routes=app.routes,
    )

    # Adiciona o esquema de segurança Bearer ao Swagger UI
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    # Aplica o esquema de segurança em todos os endpoints
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", [{"BearerAuth": []}])

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.get("/health", tags=["health"])
async def health_check():
    """
    Verifica se a API está online e funcionando.
    Usado pelo load balancer da AWS para saber se o serviço está saudável.
    """
    return {"status": "healthy", "version": "0.1.0"}
