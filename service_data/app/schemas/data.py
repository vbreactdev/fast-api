from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class Principal(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    subject: str
    issued_at: datetime
    expires_at: datetime


class ItemCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)


class ItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    description: str | None = None
    owner: str
    created_at: datetime


class ItemListResponse(BaseModel):
    items: list[ItemResponse]
    count: int

