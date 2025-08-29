jdinbot/
├── .devcontainer/                 # Development container configuration
│   ├── devcontainer.json
│   └── docker-compose.override.yml
├── .github/                       # GitHub automation
│   ├── workflows/
│   │   ├── ci.yml                # Continuous integration
│   │   ├── cd.yml                # Continuous deployment
│   │   └── security-scan.yml     # Security scanning
│   ├── dependabot.yml            # Dependency updates
│   └── ISSUE_TEMPLATE/           # Issue templates
│       ├── bug_report.md
│       └── feature_request.md
├── .vscode/                      # VS Code configuration
│   ├── settings.json
│   ├── extensions.json
│   └── launch.json
├── docker/                       # Docker-related files
│   ├── entrypoint.py            # Python entrypoint (replaced .sh)
│   ├── nginx/
│   │   └── nginx.conf           # Production nginx config
│   └── scripts/
│       ├── wait-for-it.sh       # Service dependency checker
│       └── init-db.sh           # Database initialization
├── docs/                         # Project documentation
│   ├── api/                     # API documentation
│   ├── development.md
│   ├── deployment.md
│   └── architecture.md
├── src/                          # Source code
│   └── jdinbot/                 # Package name matches project (better practice)
│       ├── __init__.py
│       ├── main.py              # FastAPI application factory
│       ├── asgi.py              # ASGI application entry point
│       ├── core/                # Core application components
│       │   ├── __init__.py
│       │   ├── config.py        # Configuration management
│       │   ├── logging.py       # Structured logging setup
│       │   ├── security.py      # Security utilities
│       │   └── exceptions.py    # Custom exceptions
│       ├── api/                 # API routes
│       │   ├── __init__.py
│       │   ├── deps.py          # API dependencies
│       │   └── v1/              # API versioning
│       │       ├── __init__.py
│       │       ├── endpoints/   # Route handlers
│       │       │   ├── __init__.py
│       │       │   ├── health.py
│       │       │   ├── users.py
│       │       │   └── transactions.py
│       │       ├── routers.py   # Router definitions
│       │       └── schemas.py   # Pydantic models
│       ├── bot/                 # Telegram bot components
│       │   ├── __init__.py
│       │   ├── dispatcher.py    # Bot dispatcher setup
│       │   ├── loader.py        # Module loader
│       │   ├── filters/         # Custom filters
│       │   ├── handlers/        # Message handlers
│       │   │   ├── __init__.py
│       │   │   ├── commands/    # Command handlers
│       │   │   │   ├── __init__.py
│       │   │   │   ├── start.py
│       │   │   │   ├── balance.py
│       │   │   │   ├── transfer.py
│       │   │   │   └── admin.py
│       │   │   └── callbacks/   # Callback query handlers
│       │   │       └── __init__.py
│       │   ├── middlewares/     # Bot middlewares
│       │   │   ├── __init__.py
│       │   │   ├── logging.py
│       │   │   └── database.py
│       │   ├── keyboards/       # Reply and inline keyboards
│       │   │   ├── __init__.py
│       │   │   ├── main.py
│       │   │   └── admin.py
│       │   └── services/        # Bot services
│       │       ├── __init__.py
│       │       └── telegram.py  # Telegram API wrapper
│       ├── db/                  # Database components
│       │   ├── __init__.py
│       │   ├── crud.py 
│       │   ├── base.py          # Declarative base
│       │   ├── session.py       # Async session factory
│       │   ├── engine.py        # Database engine
│       │   ├── models/          # Database models
│       │   │   ├── __init__.py
│       │   │   ├── user.py
│       │   │   ├── transaction.py
│       │   │   └── base.py      # Base model mixins
│       │   ├── repositories/    # Data access layer
│       │   │   ├── __init__.py
│       │   │   ├── user.py
│       │   │   └── transaction.py
│       │   └── migrations/      # Alembic migrations (integrated)
│       │       ├── versions/
│       │       ├── env.py
│       │       └── script.py.mako
│       ├── services/            # Business logic services
│       │   ├── __init__.py
│       │   ├── user.py
│       │   ├── transaction.py
│       │   └── notification.py  # Notification service
│       ├── tasks/               # Background tasks
│       │   ├── __init__.py
│       │   ├── celery.py        # Celery configuration
│       │   └── periodic.py      # Periodic tasks
│       ├── utils/               # Utility functions
│       │   ├── __init__.py
│       │   ├── money.py         # Money handling utilities
│       │   ├── validators.py    # Data validators
│       │   └── helpers.py       # Helper functions
│       └── types/               # Custom type definitions
│           └── __init__.py
├── tests/                       # Test suite
│   ├── __init__.py
│   ├── conftest.py              # pytest fixtures
│   ├── unit/                    # Unit tests
│   │   ├── __init__.py
│   │   ├── test_models.py
│   │   ├── test_services.py
│   │   └── test_utils.py
│   ├── integration/             # Integration tests
│   │   ├── __init__.py
│   │   ├── test_api.py
│   │   └── test_bot.py
│   └── e2e/                     # End-to-end tests
│       └── __init__.py
├── scripts/                     # Automation scripts
│   ├── setup.sh                 # Project setup script
│   ├── deploy.sh                # Deployment script
│   ├── test.sh                  # Test runner
│   ├── lint.sh                  # Linting script
│   └── migrate.sh               # Database migration helper
├── docker-compose.yml           # Base docker-compose
├── docker-compose.dev.yml  # Development overrides
├── docker-compose.prod.yml      # Production configuration
├── Dockerfile                   # Multi-stage Dockerfile
├── pyproject.toml               # Project configuration
├── .env.example                 # Environment variables template
├── .env                         # Local environment (gitignored)
├── .python-version              # Python version specification
├── .pre-commit-config.yaml      # Pre-commit hooks
├── Makefile                     # Task automation
├── README.md                    # Project documentation
├── LICENSE                      # License file
├── CHANGELOG.md                 # Change log
├── CONTRIBUTING.md              # Contribution guidelines
├── CODE_OF_CONDUCT.md           # Community guidelines
└── SECURITY.md                  # Security policy