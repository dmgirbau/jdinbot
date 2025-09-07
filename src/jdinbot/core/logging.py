import logging
import sys
from typing import Any

import structlog
from structlog.stdlib import LoggerFactory
from structlog.types import Processor

def configure_logging() -> None:
    """Configure structlog for structured logging with JSON output in production."""
    # Shared processors for all environments
    processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer() if ENV == "production" else structlog.dev.ConsoleRenderer(),
    ]

    structlog.configure(
        processors=processors,
        context_class=dict,
        logger_factory=LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # Configure standard logging to integrate with structlog
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.DEBUG if ENV == "development" else logging.INFO,
    )

def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """Get a structlog logger with the given name."""
    return structlog.get_logger(name)

# Initialize logging configuration
from jdinbot.core.config import ENV  # Assuming ENV is defined in config.py
configure_logging()

"""
**Key Points**:
- Uses `structlog` with `stdlib` integration for compatibility with standard Python logging.
- Outputs JSON logs in production (`ENV=production`) and human-readable logs in development (`ENV=development`), aligning with your `docker-compose.yml` and `docker-compose.prod.yml` setups.
- Includes processors for timestamps, log levels, and context variables to provide rich metadata.
- Assumes `ENV` is defined in `src/jdinbot/core/config.py` (based on `pydantic-settings` in `pyproject.toml`).

If your existing `logging.py` differs significantly, please provide it, and I’ll adjust the implementation.
"""