# Exam Integrity System - API Service

This service is built with FastAPI and managed using `uv`.

## Setup & Installation

1. Make sure you have Python 3.11.8 installed (see `.python-version`).

2. Copy env file (from project root):

   ```bash
   cp infra/.env.example infra/.env
   ```

   Or from `services/api`:

   ```bash
   cp ../../infra/.env.example ../../infra/.env
   ```

3. Run `uv sync` to install all pinned dependencies:

   ```bash
   uv sync
   ```

4. Run the API:

   ```bash
   uv run uvicorn main:app --reload --port 8000
   ```

   Health checks:

   ```bash
   curl http://localhost:8000/api/v1/health
   # {"status":"ok"}
   curl -i http://localhost:8000/health
   # 307 -> /api/v1/health
   ```

## Project Structure

```
services/api/
  main.py              # FastAPI app + /api/v1/health + /health + CORS
  core/config.py       # pydantic-settings (env_file: ../infra/.env)
  routers/             # endpoint modules (M0-16)
  models/              # DB models (M0-18)
  schemas/             # Pydantic schemas
```

See `docs/milestones/M0_IMPLEMENTATION_PLAN.md:131` (M0-14) and `docs/API_CONTRACT.md` for contract.
