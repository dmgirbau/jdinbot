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


### Requirements
- Python 3.11+
- Docker & Docker Compose


### Run with Docker Compose
```bash
docker-compose up --build
```
The bot will connect to Telegram and expose a REST API at http://localhost:8000.

### Run locally
```bash
pip install -r requirements.txt
cp .env.example .env  # fill in your TELEGRAM_TOKEN and DB details
uvicorn app.main:app --reload
```
### Database migrations
```bash
alembic revision --autogenerate -m "init schema"
alembic upgrade head
```
## Contribution Guide

We welcome contributions! Please:

* Open an issue for discussion before major changes

* Follow PEP8 style guide

* Run black, ruff, and mypy before committing

* Write tests for new features

## Security

* Secrets must be kept in .env files or environment variables

* Do not hardcode API keys or credentials

* Use least privilege when deploying in production

## Roadmap




## License

This project is open-source under the MIT License.