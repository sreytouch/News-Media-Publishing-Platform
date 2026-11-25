from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import get_settings
from app.core.exceptions import (
    AuthenticationError,
    EntityNotFoundError,
    NmppError,
    ValidationError,
)
from app.infrastructure.db.base import Base
from app.infrastructure.db.seed import seed_database
from app.infrastructure.db.session import SessionLocal, engine
from app.presentation.api.v1.router import api_router

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Import models so their tables are registered on the metadata.
    import app.infrastructure.db.models  # noqa: F401

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    if settings.seed_on_startup:
        async with SessionLocal() as session:
            await seed_database(session)
    yield


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    version="0.1.0",
    openapi_url=f"{settings.api_v1_prefix}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.get("/health", tags=["Health"])
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.exception_handler(EntityNotFoundError)
async def entity_not_found_handler(_: Request, exc: EntityNotFoundError) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(AuthenticationError)
async def authentication_error_handler(_: Request, exc: AuthenticationError) -> JSONResponse:
    return JSONResponse(status_code=401, content={"detail": str(exc)})


@app.exception_handler(ValidationError)
async def validation_error_handler(_: Request, exc: ValidationError) -> JSONResponse:
    return JSONResponse(status_code=400, content={"detail": str(exc)})


@app.exception_handler(NmppError)
async def nmpp_error_handler(_: Request, exc: NmppError) -> JSONResponse:
    return JSONResponse(status_code=500, content={"detail": str(exc)})
