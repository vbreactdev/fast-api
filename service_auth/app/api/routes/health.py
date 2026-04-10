from fastapi import APIRouter, Depends

from app.core.config import Settings, get_settings
from app.schemas.health import HealthStatus

router = APIRouter(prefix="/health", tags=["health"])


def get_settings_dependency() -> Settings:
    return get_settings()


@router.get("/live", response_model=HealthStatus, summary="Liveness probe")
async def liveness(
    settings: Settings = Depends(get_settings_dependency),
) -> HealthStatus:
    return HealthStatus(status="ok", service=settings.app_name)


@router.get("/ready", response_model=HealthStatus, summary="Readiness probe")
async def readiness(
    settings: Settings = Depends(get_settings_dependency),
) -> HealthStatus:
    return HealthStatus(status="ok", service=settings.app_name)

