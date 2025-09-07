
# syntax=docker/dockerfile:1.4
ARG PYTHON_VERSION=3.13
ARG POETRY_VERSION=2.1.4
ARG APP_USER=dino
ARG APP_UID=1001
ARG APP_GID=1001

########################
### Builder stage
########################
FROM python:${PYTHON_VERSION}-slim AS builder

# essential build deps
ENV DEBIAN_FRONTEND=noninteractive \
    POETRY_HOME=/opt/poetry \
    PATH=/opt/poetry/bin:$PATH \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update \
  && apt-get install -y --no-install-recommends curl build-essential git gcc libpq-dev ca-certificates \
  && rm -rf /var/lib/apt/lists/*

# Install Poetry (official installer)
RUN curl -sSL https://install.python-poetry.org | python3 - \
  && poetry --version

WORKDIR /app

# Copy dependency manifests for caching, copy README and source code for editable installs
COPY pyproject.toml poetry.lock* README.md src/ /app/

# Use BuildKit cache for Poetry and pip caches (speeds up repeated builds)
RUN --mount=type=cache,target=/root/.cache/pypoetry \
    --mount=type=cache,target=/root/.cache/pip \
    poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --only main

# Copy rest of the project
COPY . /app

# (optional) run tests / build steps for compiled deps here

########################
### Runtime stage
########################
FROM python:${PYTHON_VERSION}-slim AS runtime
ARG APP_USER
ARG APP_UID
ARG APP_GID

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH=/home/${APP_USER}/.local/bin:$PATH \
    APP_UID=${APP_UID} \
    APP_GID=${APP_GID}

# minimal runtime deps
RUN apt-get update \
  && apt-get install -y --no-install-recommends ca-certificates gosu netcat-openbsd \
  && rm -rf /var/lib/apt/lists/*

# Create non-root user & group (use build args so CI can override if needed)
RUN groupadd -g ${APP_GID} ${APP_USER} || true \
 && useradd --uid ${APP_UID} --gid ${APP_GID} --create-home --shell /bin/sh ${APP_USER} || true

WORKDIR /app

# Copy site-packages installed by builder (we asked Poetry to install into system site-packages)
COPY --from=builder /usr/local/lib/python${PYTHON_VERSION%.*}/site-packages /usr/local/lib/python${PYTHON_VERSION%.*}/site-packages
COPY --from=builder /app /app

# ensure ownership
RUN chown -R ${APP_USER}:${APP_USER} /app

# add a tiny entrypoint that handles signals
COPY ./docker/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Health check for FastAPI /health endpoint
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl --fail http://localhost:8000/health || exit 1

USER ${APP_USER}
ENV HOME=/home/${APP_USER}

EXPOSE 8000
ENTRYPOINT ["entrypoint.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
