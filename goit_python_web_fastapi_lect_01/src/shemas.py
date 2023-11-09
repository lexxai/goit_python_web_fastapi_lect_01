from datetime import datetime
from typing import Any, Optional, Annotated
from fastapi import Form

from pydantic import BaseModel, Field, EmailStr


class UserModel(BaseModel):
    username: str
    password: str
    # grant_type: Optional[Any] = None
    # scope: Optional[str] = None
    # client_id: Optional[Any] = None
    # client_secret: Optional[Any] = None


class NewUserResponse(BaseModel):
    username: str


class AccessTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: Optional[str] = None


class OwnerModel(BaseModel):
    email: EmailStr
    # email: str = Field(default="email@examole.com", pattern=r'^\w+@\w+\.\w+$')


class OwnerResponse(BaseModel):
    id: int = 1
    email: EmailStr
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CatModel(BaseModel):
    nickname: str = Field("Lukas", min_length=3, max_length=16)
    age: int = Field(1, ge=0, le=30)
    description: str
    vaccinated: bool = False
    owner_id: int = Field(1, gt=0)


class CatVactinatedModel(BaseModel):
    vaccinated: bool = False


class CatResponse(BaseModel):
    id: int
    nickname: str
    age: int
    description: str
    vaccinated: bool
    owner: OwnerResponse

    class Config:
        from_attributes = True
