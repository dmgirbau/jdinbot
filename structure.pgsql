jdinbot/
├─ .devcontainer/
│  └─ devcontainer.json
├─ docker/
│  └─ entrypoint.sh
├─ .github/
│  ├─ workflows/
│  │  └─ ci.yml
│  └─ dependabot.yml
├─ src/
│  └─ app/
│     ├─ __init__.py
│     ├─ main.py                  # FastAPI application
│     ├─ core/
│     │  ├─ config.py
│     │  └─ logging.py
│     ├─ api/
│     │  ├─ http.py
│     │  └─ v1/
│     │     ├─ routers.py
│     │     └─ schemas.py
│     ├─ bot/
│     │  ├─ __init__.py
│     │  ├─ dispatcher.py
│     │  ├─ commands.py
│     │  ├─ handlers/
│     │  │  ├─ __init__.py
│     │  │  ├─ common.py
│     │  │  ├─ start.py
│     │  │  └─ admin.py
│     │  ├─ middlewares.py
│     │  ├─ keyboards.py
│     │  └─ bot.py
│     ├─ db/
│     │  ├─ base.py
│     │  ├─ models/
│     │  │  ├─ __init__.py
│     │  │  └─ user.py
│     │  ├─ session.py
│     │  ├─ engine.py
│     │  └─ crud.py
│     ├─ services/
│     │  └─ telegram_service.py
│     ├─ tasks/                   # Celery / background tasks
│     └─ utils/
│        ├─ money.py
│        └─ helpers.py
├─ tests/
│  ├─ test_basic.py
│  ├─ test_gamble.py
│  └─ test_transfer.py
├─ scripts/
│  ├─ build.sh
│  └─ setup_db.sh
├─ docker-compose.dev.yml
├─ docker-compose.prod.yml
├─ docker-compose.yml
├─ Dockerfile
├─ pyproject.toml
├─ .env.example
├─ .gitignore
├─ README.md
├─ LICENSE
└─ alembic/                       # migrations (might be in src/app/db in some projects)
   ├─ env.py
   └─ versions/