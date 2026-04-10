from pydantic import BaseModel


class HealthStatus(BaseModel):
    status: str
    service: str
    dependency: str | None = None

