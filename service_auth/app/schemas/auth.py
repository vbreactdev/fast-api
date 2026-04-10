from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AccessTokenRequest(BaseModel):
    username: str = Field(min_length=3, max_length=64)
    password: str = Field(min_length=3, max_length=128)


class AccessTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenIntrospectionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    subject: str
    issued_at: datetime
    expires_at: datetime

