FROM ghcr.io/astral-sh/uv:python3.12-alpine AS worker
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

WORKDIR /app

COPY services/price-list-import-service/pyproject.toml services/price-list-import-service/uv.lock ./services/price-list-import-service/

WORKDIR /app/services/price-list-import-service
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

WORKDIR /app
COPY services/price-list-import-service/ ./services/price-list-import-service/

WORKDIR /app/services/price-list-import-service
ENV PYTHONPATH="/app/services/price-list-import-service"

CMD ["uv", "run", "python", "app/main.py"]
