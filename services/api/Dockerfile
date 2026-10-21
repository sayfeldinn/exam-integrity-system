# syntax=docker/dockerfile:1
# M0-26: API image — uv-managed deps, bytecode-compiled, no dev group.
# requires-python is pinned ==3.11.8, so the base image must match exactly.
FROM python:3.11.8-slim

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never

WORKDIR /app

# Dependency layer first (cached unless pyproject/uv.lock change)
COPY pyproject.toml uv.lock ./
RUN pip install --no-cache-dir uv && uv sync --frozen --no-dev

COPY . .

EXPOSE 8000
CMD ["uv", "run", "--no-sync", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
