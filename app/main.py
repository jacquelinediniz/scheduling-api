from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

# Importa todos os models para o SQLAlchemy registrá-los corretamente
from app.models import tenant, user, service, availability, appointment  # noqa: F401
from app.api.v1.endpoints import appointments, auth, services, tenants

app = FastAPI(
    title="Scheduling API",
    description="Multi-tenant scheduling API for businesses",
    version="0.1.0",
)

app.include_router(tenants.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(services.router, prefix="/api/v1")
app.include_router(appointments.router, prefix="/api/v1")


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Scheduling API",
        version="0.1.0",
        description="Multi-tenant scheduling API for businesses",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", [{"BearerAuth": []}])
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "healthy", "version": "0.1.0"}
