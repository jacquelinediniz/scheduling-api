from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Configurações centrais da aplicação.
    Os valores são lidos automaticamente das variáveis de ambiente
    ou do arquivo .env na raiz do projeto.
    """

    # Banco de dados
    database_url: str

    # API
    secret_key: str = "development-secret-key"
    environment: str = "development"
    debug: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = False


# Instância única das configurações — importada em todo o projeto
settings = Settings()
