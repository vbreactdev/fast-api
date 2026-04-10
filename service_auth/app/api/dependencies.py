import hmac
from typing import Annotated

from fastapi import Depends, Header, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import Settings, get_settings
from app.services.token_service import TokenService

bearer_scheme = HTTPBearer(auto_error=False)


def get_token_service(request: Request) -> TokenService:
    return request.app.state.token_service


def get_settings_dependency() -> Settings:
    return get_settings()


def verify_internal_api_key(
    x_internal_api_key: Annotated[str | None, Header(alias="X-Internal-Api-Key")] = None,
    settings: Settings = Depends(get_settings_dependency),
) -> None:
    if x_internal_api_key is None or not hmac.compare_digest(
        x_internal_api_key, settings.internal_api_key
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid internal API key.",
        )


def get_bearer_credentials(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> HTTPAuthorizationCredentials:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing bearer token.",
        )
    return credentials

