# python-base sets up all our shared environment variables
FROM python:3.12-slim as python-base

# python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    # poetry
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    \
    # paths
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        build-essential

# install poetry
RUN pip install poetry

# install postgres dependencies inside of Docker
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

# Definir o diretório onde será instalado o projeto
WORKDIR $PYSETUP_PATH

# Copiar os arquivos de dependências antes para otimizar o cache
COPY poetry.lock pyproject.toml ./
COPY README.md ./

# Copiar o código do projeto ANTES da instalação
COPY . .

# Instalar as dependências e o próprio projeto
RUN poetry install

# Expor a porta padrão do Django
EXPOSE 8000

# Comando de inicialização (produção/Heroku)
CMD gunicorn bookstore.wsgi:application --bind 0.0.0.0:$PORT
