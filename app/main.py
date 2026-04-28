from fastapi import FastAPI

app = FastAPI(
    title="Scheduling API",
    description="Multi-tenant scheduling API for businesses",
    version="0.1.0",
)


@app.get("/health", tags=["health"])
async def health_check():
    """
    Verifica se a API está online e funcionando.
    Usado pelo load balancer da AWS para saber se o serviço está saudável.
    """
    return {"status": "healthy", "version": "0.1.0"}
