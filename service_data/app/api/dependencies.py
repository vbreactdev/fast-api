from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.clients.auth_service import (
    AuthenticationError,
    AuthServiceClient,
    UpstreamServiceError,
)
from app.schemas.data import Principal
from app.services.repository import InMemoryItemRepository

bearer_scheme = HTTPBearer(auto_error=False)


def get_auth_client(request: Request) -> AuthServiceClient:
    return request.app.state.auth_client


def get_item_repository(request: Request) -> InMemoryItemRepository:
    return request.app.state.item_repository


async def get_current_principal(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    auth_client: AuthServiceClient = Depends(get_auth_client),
) -> Principal:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing bearer token.",
        )

    try:
        return await auth_client.introspect_token(credentials.credentials)
    except AuthenticationError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc
    except UpstreamServiceError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc

