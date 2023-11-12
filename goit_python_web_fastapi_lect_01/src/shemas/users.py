from datetime import datetime
from enum import Enum
from typing import Any, Optional, Annotated
from fastapi import Form

from pydantic import BaseModel, Field, EmailStr
from sqlalchemy import Column, String

from src.database.models import Role


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


class NewUserResponse(BaseModel):
    username: str

class roles(str):
    ...


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    avatar: str | None
    # roles: roles | str

    class Config:
        from_attributes = True
