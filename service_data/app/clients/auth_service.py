from __future__ import annotations

import httpx

from app.schemas.data import Principal


class AuthenticationError(Exception):
    pass


class UpstreamServiceError(Exception):
    pass


class AuthServiceClient:
    def __init__(
        self,
        http_client: httpx.AsyncClient,
        base_url: str,
        internal_api_key: str,
    ) -> None:
        self._http_client = http_client
        self._base_url = base_url.rstrip("/")
        self._internal_api_key = internal_api_key

    async def introspect_token(self, token: str) -> Principal:
        try:
            response = await self._http_client.get(
                f"{self._base_url}/api/v1/auth/introspect",
                headers={
                    "Authorization": f"Bearer {token}",
                    "X-Internal-Api-Key": self._internal_api_key,
                },
            )
        except httpx.HTTPError as exc:
            raise UpstreamServiceError("Auth service is unavailable.") from exc

        if response.status_code == 401:
            raise AuthenticationError("Invalid or expired bearer token.")
        if response.status_code == 403:
            raise UpstreamServiceError("Auth service rejected the internal API key.")
        if response.is_error:
            raise UpstreamServiceError("Auth service returned an unexpected error.")

        return Principal.model_validate(response.json())

    async def check_health(self) -> None:
        try:
            response = await self._http_client.get(f"{self._base_url}/health/ready")
        except httpx.HTTPError as exc:
            raise UpstreamServiceError("Auth readiness check failed.") from exc

        if response.status_code != 200:
            raise UpstreamServiceError("Auth service is not ready.")

