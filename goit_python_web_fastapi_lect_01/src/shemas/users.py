from datetime import datetime
from typing import Any, Optional, Annotated
from fastapi import Form

from pydantic import BaseModel, Field, EmailStr


class NewUserResponse(BaseModel):
    username: str


class AccessTokenRefreshResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: Optional[str] = None


class AccessTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"



class UserModel(BaseModel):
    username: str
    password: str
    # grant_type: Optional[Any] = None
    # scope: Optional[str] = None
    # client_id: Optional[Any] = None
    # client_secret: Optional[Any] = None

