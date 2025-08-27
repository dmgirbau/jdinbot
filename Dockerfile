FROM python:3.12-slim


WORKDIR /app


ENV PYTHONUNBUFFERED=1


COPY pyproject.toml poetry.lock* requirements.txt* ./


# Install deps (choose poetry or pip)
RUN pip install --no-cache-dir -r requirements.txt || true


COPY . .


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]