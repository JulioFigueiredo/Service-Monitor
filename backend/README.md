# Service Monitor — Backend

Backend REST API for the Service Monitor platform, built with FastAPI, SQLAlchemy 2.0, PostgreSQL, and Pydantic.

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager
- Docker & Docker Compose (optional, for PostgreSQL and Redis)

## Setup and Installation

1. Install dependencies using `uv`:
   ```bash
   uv sync
   ```

2. Copy the environment variables template:
   ```bash
   cp ../.env.example .env
   ```

3. Run database migrations:
   ```bash
   uv run alembic upgrade head
   ```

4. Run the development server:
   ```bash
   uv run uvicorn app.main:app --reload --port 8000
   ```

5. Run test suite:
   ```bash
   uv run pytest
   ```
