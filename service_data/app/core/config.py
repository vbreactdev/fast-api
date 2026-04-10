from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field(default="service_data", validation_alias="APP_NAME")
    environment: str = Field(default="development", validation_alias="APP_ENVIRONMENT")
    host: str = Field(default="0.0.0.0", validation_alias="APP_HOST")
    port: int = Field(default=8000, validation_alias="APP_PORT")
    log_level: str = Field(default="INFO", validation_alias="LOG_LEVEL")
    auth_service_url: str = Field(
        default="http://service_auth:8000",
        validation_alias="AUTH_SERVICE_URL",
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

