FROM ghcr.io/astral-sh/uv:python3.12-alpine AS worker
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

WORKDIR /app

COPY services/notification-service/pyproject.toml services/notification-service/uv.lock ./services/notification-service/

WORKDIR /app/services/notification-service
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

WORKDIR /app
COPY services/notification-service/ ./services/notification-service/

WORKDIR /app/services/notification-service
ENV PYTHONPATH="/app/services/notification-service"

CMD ["uv", "run", "python", "app/main.py"]
