########################################
FROM node:17-alpine as web-build

WORKDIR /usr/src/app

ENV PATH /usr/src/app/node_modules/.bin:$PATH

COPY web/package.json web/package-lock.json ./
RUN npm install

COPY web/src src
COPY web/public public
COPY web/tsconfig.json web/.env ./

RUN npm run build

########################################
FROM nginx as web

COPY --from=web-build /usr/src/app/build /usr/share/nginx/html

########################################
FROM python:3.9 as poetry

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    # poetry
    POETRY_VERSION=1.1.11 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    POETRY_NO_ANSI=1 \
    \
    # paths
    PYSETUP_PATH="/opt/pysetup"

# Place poetry in PATH
ENV PATH="$POETRY_HOME/bin:$PATH"

RUN apt-get update && apt-get -y install curl \
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

########################################
FROM poetry as api

WORKDIR $PYSETUP_PATH
COPY api/poetry.lock api/pyproject.toml ./
RUN poetry install --no-dev --no-root
RUN mkdir .spotify-cache && chmod 0755 .spotify-cache

COPY api/src/api api
RUN poetry install

CMD  ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "80"]

########################################
FROM poetry as mockreader

WORKDIR $PYSETUP_PATH
COPY mockreader/poetry.lock mockreader/pyproject.toml ./
RUN poetry install --no-dev --no-root

COPY mockreader/src/app app
RUN poetry install

ENTRYPOINT [ "python", "app" ]
