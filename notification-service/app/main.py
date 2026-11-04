from contextlib import asynccontextmanager

import app.models
from app.api.v1.endpoints.orders import router as products_router
from app.core.config import settings
from app.core.exceptions import ApplicationError
from app.core.rabbitmq import broker
from app.core.redis_client import redis_async_client
from fastapi import (
    FastAPI,
    Request,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

rabbitmq_assets = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_async_client.ping()
    await broker.connect()

    yield

    await broker.close()
    await redis_async_client.close()


app = FastAPI(
    title="Product Service",
    version="1.0.0",
    lifespan=lifespan,
    debug=settings.DEBUG,
)


origins = [
    "http://localhost:8000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    products_router,
    prefix="/api/v1",
)


@app.exception_handler(ApplicationError)
async def application_error_handler(request: Request, exc: ApplicationError):
    return JSONResponse(
        status_code=exc.status_code, content={"detail": exc.detail}, headers=exc.headers
    )
