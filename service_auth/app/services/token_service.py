import hmac
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from pydantic import BaseModel

from app.core.config import Settings
from app.schemas.auth import AccessTokenResponse


class InvalidTokenError(Exception):
    pass


class TokenClaims(BaseModel):
    subject: str
    issued_at: datetime
    expires_at: datetime


class TokenService:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def authenticate_bootstrap_user(self, username: str, password: str) -> bool:
        return hmac.compare_digest(
            username, self._settings.bootstrap_username
        ) and hmac.compare_digest(password, self._settings.bootstrap_password)

    def create_access_token(self, subject: str) -> AccessTokenResponse:
        issued_at = datetime.now(timezone.utc)
        expires_at = issued_at + timedelta(
            minutes=self._settings.access_token_ttl_minutes
        )
        payload = {
            "sub": subject,
            "iat": int(issued_at.timestamp()),
            "exp": int(expires_at.timestamp()),
        }
        access_token = jwt.encode(
            payload,
            self._settings.jwt_secret,
            algorithm=self._settings.jwt_algorithm,
        )
        return AccessTokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=int((expires_at - issued_at).total_seconds()),
        )

    def decode_token(self, token: str) -> TokenClaims:
        try:
            payload = jwt.decode(
                token,
                self._settings.jwt_secret,
                algorithms=[self._settings.jwt_algorithm],
            )
        except JWTError as exc:
            raise InvalidTokenError("Unable to decode JWT.") from exc

        subject = payload.get("sub")
        issued_at = payload.get("iat")
        expires_at = payload.get("exp")
        if not subject or not issued_at or not expires_at:
            raise InvalidTokenError("JWT payload is missing required claims.")

        return TokenClaims(
            subject=str(subject),
            issued_at=datetime.fromtimestamp(int(issued_at), tz=timezone.utc),
            expires_at=datetime.fromtimestamp(int(expires_at), tz=timezone.utc),
        )
