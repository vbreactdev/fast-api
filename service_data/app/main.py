from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI

from app.api.router import api_router
from app.clients.auth_service import AuthServiceClient
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.services.repository import InMemoryItemRepository


def create_lifespan():
    @asynccontextmanager
    async def lifespan(application: FastAPI):
        settings = get_settings()
        http_client = httpx.AsyncClient(
            timeout=httpx.Timeout(5.0, connect=2.0),
            follow_redirects=False,
        )
        application.state.auth_client = AuthServiceClient(
            http_client=http_client,
            base_url=settings.auth_service_url,
            internal_api_key=settings.internal_api_key,
        )
        application.state.item_repository = InMemoryItemRepository()
        yield
        await http_client.aclose()

    return lifespan


def create_application() -> FastAPI:
    settings = get_settings()
    configure_logging(service_name=settings.app_name, log_level=settings.log_level)

    application = FastAPI(
        title=settings.app_name,
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=create_lifespan(),
    )
    application.include_router(api_router)
    return application


app = create_application()

