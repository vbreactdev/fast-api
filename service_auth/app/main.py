from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.services.token_service import TokenService


def create_application() -> FastAPI:
    settings = get_settings()
    configure_logging(service_name=settings.app_name, log_level=settings.log_level)

    application = FastAPI(
        title=settings.app_name,
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )
    application.state.token_service = TokenService(settings=settings)
    application.include_router(api_router)
    return application


app = create_application()

