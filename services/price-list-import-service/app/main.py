from contextlib import asynccontextmanager

import app.models

from app.core.config import settings
from app.core.exceptions import ApplicationError

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
    yield

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




@app.exception_handler(ApplicationError)
async def application_error_handler(request: Request, exc: ApplicationError):
    return JSONResponse(
        status_code=exc.status_code, content={"detail": exc.detail}, headers=exc.headers
    )
