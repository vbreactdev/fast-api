from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials

from app.api.dependencies import (
    get_bearer_credentials,
    get_token_service,
    verify_internal_api_key,
)
from app.schemas.auth import (
    AccessTokenRequest,
    AccessTokenResponse,
    TokenIntrospectionResponse,
)
from app.services.token_service import InvalidTokenError, TokenService

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post(
    "/token",
    response_model=AccessTokenResponse,
    summary="Issue a JWT access token",
)
async def issue_token(
    payload: AccessTokenRequest,
    token_service: TokenService = Depends(get_token_service),
) -> AccessTokenResponse:
    if not token_service.authenticate_bootstrap_user(
        username=payload.username,
        password=payload.password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password.",
        )

    return token_service.create_access_token(subject=payload.username)


@router.get(
    "/introspect",
    response_model=TokenIntrospectionResponse,
    dependencies=[Depends(verify_internal_api_key)],
    summary="Validate a bearer token for trusted internal callers",
)
async def introspect_token(
    credentials: HTTPAuthorizationCredentials = Depends(get_bearer_credentials),
    token_service: TokenService = Depends(get_token_service),
) -> TokenIntrospectionResponse:
    try:
        claims = token_service.decode_token(credentials.credentials)
    except InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token.",
        ) from exc

    return TokenIntrospectionResponse(
        subject=claims.subject,
        issued_at=claims.issued_at,
        expires_at=claims.expires_at,
    )

