FROM ghcr.io/astral-sh/uv:python3.12-alpine AS worker
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

WORKDIR /app

COPY services/document-service/pyproject.toml services/document-service/uv.lock ./services/document-service/

WORKDIR /app/services/document-service
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

WORKDIR /app
COPY services/document-service/ ./services/document-service/

WORKDIR /app/services/document-service
ENV PYTHONPATH="/app/services/document-service"

CMD ["uv", "run", "python", "app/main.py"]
