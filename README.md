# JDINBot


A modern Telegram bot built with **Python**, **FastAPI**, **aiogram**, and **PostgreSQL**. This project is designed both as a **learning project** (to explore professional-grade software practices) and as a **production-ready system** to power community interactions.


## Features
- Telegram bot built with [aiogram](https://docs.aiogram.dev)
- REST API with [FastAPI](https://fastapi.tiangolo.com)
- PostgreSQL database with async [SQLAlchemy](https://docs.sqlalchemy.org)
- Database migrations via [Alembic](https://alembic.sqlalchemy.org)
- Dockerized development setup
- Strict linting, type-checking, and testing culture
- Secure, scalable, open-source mindset


## Development Setup

## Architecture
- Python 3.11, FastAPI, aiogram
- PostgreSQL for persistent storage
- Docker multi-stage builds + Poetry-managed dependencies

## Quickstart (Development)
1. Copy configuration: `cp .env.example .env` and fill values (TELEGRAM_TOKEN, DATABASE_URL, ADMIN_CHAT_ID).
2. Start dev environment (hot reload):  
   `docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build`
3. Visit the REST API at `http://localhost:8000` and your bot in Telegram.

## Quickstart (Production)
1. Build & run production images:
   `docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d`
2. Apply database migrations:
   `docker compose exec web alembic upgrade head`  (if applicable)
```

### Database migrations
```bash
alembic revision --autogenerate -m "init schema"
alembic upgrade head
```
## Contribution Guide

- See `CONTRIBUTING.md` for details. TL;DR:
  - Tests required for new features.
  - Document public API or bot commands in `docs/`.
  - Use small, focused PRs.

We welcome contributions! Please:

* Follow PEP8 style guide

## Development workflow (recommended)
- Create an issue before major changes.
- Open a feature branch `feature/short-description`.
- Run formatters & linters before pushing: `black . && ruff check . && mypy .`
- Create a Pull Request referencing the issue; request 1+ reviews.

## Security

* Secrets must be kept in .env files or environment variables

* Do not hardcode API keys or credentials

* Use least privilege when deploying in production

* Report security issues privately following `SECURITY.md`.

## FAQ / Troubleshooting
- If you get permission issues when mounting code in dev, set `UID`/`GID` env vars (e.g. `export UID=$(id -u) GID=$(id -g)`).

## Community & Governance
- Use GitHub Issues for bugs & feature requests.
- Use Discussions (or a Telegram/Matrix room) for design conversations.
- Maintain a `MAINTAINERS.md` and a `CODEOWNERS` file so community knows who to ping for reviews.


## Roadmap




## License

This project is open-source under the MIT License.