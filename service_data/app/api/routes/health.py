from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_auth_client
from app.clients.auth_service import AuthServiceClient, UpstreamServiceError
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
    auth_client: AuthServiceClient = Depends(get_auth_client),
) -> HealthStatus:
    try:
        await auth_client.check_health()
    except UpstreamServiceError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc

    return HealthStatus(status="ok", service=settings.app_name, dependency="service_auth")

