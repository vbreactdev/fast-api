from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field(default="service_auth", validation_alias="APP_NAME")
    environment: str = Field(default="development", validation_alias="APP_ENVIRONMENT")
    host: str = Field(default="0.0.0.0", validation_alias="APP_HOST")
    port: int = Field(default=8000, validation_alias="APP_PORT")
    log_level: str = Field(default="INFO", validation_alias="LOG_LEVEL")
    bootstrap_username: str = Field(
        default="admin",
        validation_alias="AUTH_BOOTSTRAP_USERNAME",
    )
    bootstrap_password: str = Field(
        default="changeit",
        validation_alias="AUTH_BOOTSTRAP_PASSWORD",
    )
    jwt_secret: str = Field(
        default="change-this-secret-in-production",
        validation_alias="AUTH_JWT_SECRET",
    )
    jwt_algorithm: str = Field(default="HS256", validation_alias="AUTH_JWT_ALGORITHM")
    access_token_ttl_minutes: int = Field(
        default=60,
        validation_alias="AUTH_ACCESS_TOKEN_TTL_MINUTES",
    )
    internal_api_key: str = Field(
        default="internal-dev-key",
        validation_alias="INTERNAL_API_KEY",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()

