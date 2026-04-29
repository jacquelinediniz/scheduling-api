# Imagem base — Python 3.13 na versão slim (menor tamanho, sem pacotes desnecessários)
FROM python:3.13-slim

# Define o diretório de trabalho dentro do container
# Todos os comandos seguintes rodam a partir daqui
WORKDIR /app

# Instala o Poetry
RUN pip install poetry==2.3.4

# Copia apenas os arquivos de dependências primeiro
# Isso aproveita o cache do Docker — se as dependências não mudaram,
# o Docker não precisa reinstalar tudo a cada build
COPY pyproject.toml poetry.lock ./

# Instala as dependências sem criar ambiente virtual
# dentro do container não precisamos de venv — o container já é isolado
RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-root

# Copia o resto do código
COPY . .

# Expõe a porta 8000 para o mundo externo
EXPOSE 8000

# Comando que roda quando o container inicia
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]