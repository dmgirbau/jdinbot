# Contributing to JDINBot


We’re excited you want to contribute! This project is both a **learning space** and a **production-ready system**, so we value contributions that improve quality and maintainability.


## Getting Started
1. Fork the repository and clone your fork
2. Create a new branch: `git checkout -b feature/my-feature`
3. Install dependencies: `pip install -r requirements.txt`
4. Copy `.env.example` → `.env` and fill in secrets (Telegram token, DB URL)
5. Run services with Docker: `docker-compose up`


## Code Style
- Follow [PEP8](https://peps.python.org/pep-0008/)
- Use [black](https://github.com/psf/black) for formatting
- Use [ruff](https://github.com/astral-sh/ruff) for linting
- Use [mypy](http://mypy-lang.org/) for type checks
- Security scanning with [bandit](https://github.com/PyCQA/bandit)


Run all checks:
```bash
black .
ruff check .
mypy .
pytest
```

## Pull Requests

* Write clear commit messages

* Reference related issues (Fixes #123)

* Ensure tests pass in CI before requesting review

* Keep PRs focused (small and atomic)

## Testing

We use pytest and pytest-asyncio. New features should include test coverage.
```bash
pytest --cov=app
```
## Communication

* Use GitHub Issues for bugs and feature requests

* Use GitHub Discussions (if enabled) for broader topics
--- 
Thanks for helping us build a robust, professional, and welcoming community around JDINBot!

## Next Steps
- Add `.env.example`
- Write GitHub Actions workflow (`.github/workflows/ci.yml`)
- Set up pre-commit hooks