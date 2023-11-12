from datetime import datetime
from typing import Any, Optional, Annotated
from fastapi import Form

from pydantic import BaseModel, Field, EmailStr
from sqlalchemy import Column, String


class AccessTokenRefreshResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: str


class AccessTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserModel(BaseModel):
    username: str = Field(min_length=6, max_length=150)
    email: EmailStr
    password: str = Field(min_length=6, max_length=32)
    # grant_type: Optional[Any] = None
    # scope: Optional[str] = None
    # client_id: Optional[Any] = None
    # client_secret: Optional[Any] = None


class NewUserResponse(BaseModel):
    username: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    avatar: Optional[str|None] = None

    class Config:
        from_attributes = True
