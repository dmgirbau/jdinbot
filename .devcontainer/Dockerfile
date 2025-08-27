# ===== Base image =====
FROM python:3.13-slim AS base

# ===== System dependencies =====
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

# ===== Install Poetry =====
ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN curl -sSL https://install.python-poetry.org | python3 -

# ===== Set working directory =====
WORKDIR "/workspaces/jdinbot"

# ===== Copy dependency files first (caching) =====
COPY pyproject.toml poetry.lock* /app/

# ===== Build argument to switch modes =====
ARG DEV_MODE=true

# ===== Install dependencies =====
RUN if [ "$DEV_MODE" = "true" ]; then \
        # Dev mode: virtualenv inside project \
        poetry config virtualenvs.in-project true && \
        poetry install --no-root --only main; \
    else \
        # Prod mode: global installation \
        poetry config virtualenvs.create false && \
        poetry install --no-root --only main; \
    fi

# ===== Copy source code =====
COPY . /app

# ===== Install current project =====
RUN if [ "$DEV_MODE" = "true" ]; then \
        poetry install --editable; \
    else \
        poetry install; \
    fi

# ===== Default command =====
CMD ["poetry", "run", "python", "bot.py"]  # adjust to your entry script

# ===== Final stage =====
FROM base AS final