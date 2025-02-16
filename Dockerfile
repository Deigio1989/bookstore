# Use Python 3.12 como imagem base
FROM python:3.12-slim AS python-base

# Variáveis de ambiente para Python e Poetry
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.6.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

# Adicionar Poetry e o virtualenv ao PATH
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# Instalar dependências necessárias
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        build-essential

# Instalar o Poetry especificando a versão
RUN curl -sSL https://install.python-poetry.org | python3 - --version $POETRY_VERSION

# Instalar dependências do PostgreSQL
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

# Copiar arquivos de configuração do Poetry
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./
COPY README.md ./

# Verificar se os arquivos foram copiados corretamente
RUN ls -la $PYSETUP_PATH

# Instalar dependências do projeto usando o Poetry
RUN poetry install  

WORKDIR /app

# Copiar o código do projeto
COPY . /app/

# Expor a porta 8000
EXPOSE 8000

# Comando para rodar a aplicação
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
