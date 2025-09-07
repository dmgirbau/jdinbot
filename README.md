# JDINBot

A modern Telegram bot built with **Python**, **FastAPI**, **aiogram**, and **PostgreSQL**. This project is designed both as a **learning project** (to explore professional-grade software practices) and as a **production-ready system** to power community interactions.

[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/dmgirbau/jdinbot)

## Features

- Telegram bot built with [aiogram](https://docs.aiogram.dev)
- REST API with [FastAPI](https://fastapi.tiangolo.com)
- PostgreSQL database with async [SQLAlchemy](https://docs.sqlalchemy.org)
- Database migrations via [Alembic](https://alembic.sqlalchemy.org)
- Dockerized development setup
- Strict linting, type-checking, and testing culture
- Secure, scalable, open-source mindset

## Architecture

JDINBot is built with a modern, scalable architecture designed for high performance and maintainability:

### Core Technologies

- **Python 3.13** with full async/await support
- **FastAPI** for high-performance REST API endpoints with automatic OpenAPI documentation
- **Aiogram 3.x** for modern Telegram Bot API integration
- **PostgreSQL 16** with async support via asyncpg for persistent storage
- **SQLAlchemy 2.0** with async ORM capabilities
- **Poetry** for dependency management and packaging

### Infrastructure & Tooling

- **Docker** with multi-stage builds for optimized containerization
- **Docker Compose** for local development and production deployments
- **VS Code DevContainers** for consistent development environments
- **Alembic** for database migrations with autogenerate support
- **Structlog** for structured, production-ready logging with JSON output in production and detailed error logging for database connectivity issues
- **Prometheus** integration for metrics and monitoring

### Code Quality & Security

- **Ruff** for ultra-fast linting and formatting
- **Mypy** for strict static type checking
- **Black** for consistent code formatting
- **Pytest** with async support for comprehensive testing
- **Bandit** for security scanning
- **Pre-commit hooks** for quality control

### Project Structure

The project follows a modular `src` layout with clear separation of concerns:

- `src/jdinbot/core/` - Configuration and foundational utilities
- `src/jdinbot/api/` - FastAPI routes and REST endpoints  
- `src/jdinbot/bot/` - Telegram bot handlers and middleware
- `src/jdinbot/db/` - Database models and async session management
- `src/jdinbot/services/` - Business logic and external integrations
- `src/jdinbot/tasks` - Background tasks
- `src/jdinbot/utils/` - Shared utilities and helpers
- `src/jdinbot/types/` - Custom type definitions

This architecture ensures the application is:

- **Highly scalable** with async-first design
- **Type-safe** with comprehensive static analysis
- **Well-tested** with extensive test coverage
- **Production-ready** with proper logging and monitoring
- **Developer-friendly** with consistent tooling and environments
- **Secure** with built-in security scanning and best practices

## Development Setup

### Quickstart (Development)

- `POSTGRES_PORT`: The port for the PostgreSQL service (default: 5432). In development, this port is exposed on the host. In production, consider not exposing it for security.

1. Copy configuration: `cp .env.example .env` and fill values for `TELEGRAM_TOKEN`, `WEBHOOK_SECRET_PATH`, `ENV`, `ADMIN_CHAT_ID`, `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_DB`, `POSTGRES_USER`, and `POSTGRES_PASSWORD`.
2. Start dev environment (hot reload):  
   `docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build`
3. The bot service will wait for the PostgreSQL database to be ready before starting.
4. Visit the REST API at `http://localhost:8000` and your bot in Telegram.

### Quickstart (Production)

1. Build & run production images:
   `docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d`
2. Apply database migrations:
   `docker compose exec bot alembic upgrade head`
3. The bot service will wait for the PostgreSQL database to be ready before starting.

### VS Code DevContainer

This project includes a DevContainer configuration for VS Code. To use it:

1. Install the Dev Containers extension in VS Code
2. Open the command palette (Ctrl+Shift+P) and select "Dev Containers: Reopen in Container"
3. The container will build and setup the development environment automatically

### Database migrations

Migrations are handled via Alembic. To create and apply migrations:

```bash
# Create a new migration
docker compose exec bot alembic revision --autogenerate -m "description"

# Apply migrations
docker compose exec bot alembic upgrade head
```

## Contribution Guideline

- See `CONTRIBUTING.md` for details. TL;DR:
- Tests required for new features.
- Document public API or bot commands in `docs/`.
- Use small, focused PRs.

We welcome contributions! Please:

- Follow PEP8 style guide.

### Development workflow (recommended)

- Create an issue before major changes.
- Open a feature branch `feature/short-description`
- Run formatters & linters before pushing:

  ```bash
  black .
  ruff check .
  mypy .

-Create a Pull Request referencing the issue; request 1+ reviews.

### Security

- Secrets must be kept in .env files or environment variables

- Do not hardcode API keys or credentials

- Use least privilege when deploying in production

- Report security issues privately following `SECURITY.md`.

### FAQ / Troubleshooting

- If you get permission issues when mounting code in dev, set `UID`/`GID` env vars (e.g. `export UID=$(id -u) GID=$(id -g)`).
- **Database connection issues**: Check the `bot` service logs (`docker compose logs bot`) for structured error messages if the application fails to connect to PostgreSQL. Ensure `.env` variables (`POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`) are correctly set.

### Community & Governance

- Use GitHub Issues for bugs & feature requests.
- Use Discussions (or a Telegram/Matrix room) for design conversations.
- Maintain a `MAINTAINERS.md` and a `CODEOWNERS` file so community knows who to ping for reviews.

## Roadmap

JDINBot is designed as a layered system: minimal features today, professional scaffolding for growth tomorrow.

- **M1 – Local MVP (Now)**  
  Run the bot locally with Docker Compose.  
  Features: `/start` command, `/balance`, persistent Postgres storage.  

- **M2 – Core Features (Next)**  
  Implement user economy: `/transfer`, admin commands (`/promote`, `/ban`).  
  Add REST API endpoints (`/health`, `/users`).  

- **M3 – Quality & Tooling (Soon)**  
  Introduce automated linting, type-checking, and tests.  
  Align dev and prod environments with Docker.  

- **M4 – Scaling Up (Future)**  
  Enable CI/CD pipelines, monitoring with Prometheus, contribution guidelines.  
  Secure and professionalize infrastructure for multi-developer collaboration.  

### License

This project is open-source under the MIT License.
