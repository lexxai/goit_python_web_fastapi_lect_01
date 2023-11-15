import pickle
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
import redis as redis
from os import environ

from src.database.db import get_db
from src.database.models import User
from .auth_token import AuthToken
from src.repository import users as repository_users
from src.shemas.auth import AccessTokenRefreshResponse


class Auth(AuthToken):
    auth_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
    auth_response_model = OAuth2PasswordRequestForm
    token_response_model = AccessTokenRefreshResponse
    r = redis.Redis(host=environ.get("REDIS_HOST","localhost"), port=int(environ.get("REDIS_PORT",6379)), db=0)

    # define a function to generate a new refresh token
    def create_refresh_token(self, data: dict, expires_delta: Optional[float] = None) -> tuple[str, datetime]:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(days=7)
        expire = expire.replace(tzinfo=timezone.utc)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "refresh_token"})
        encoded_refresh_token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_refresh_token, expire

    def decode_refresh_token(self, refresh_token: str):
        try:
            payload = jwt.decode(refresh_token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload["scope"] == "refresh_token":
                email = payload["sub"]
                return email
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid scope for token",
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )

    def create_email_token(self, data: dict, expires_delta: Optional[float] = None) -> str | None:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(days=7)
        expire = expire.replace(tzinfo=timezone.utc)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "email_token"})
        encoded_token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_token

    def get_email_from_token(self, token: str) -> str | None:
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload and payload["scope"] == "email_token":
                email = payload.get("sub")
                return email
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid scope for token",
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
        
    def refresh_access_token(self, refresh_token: str) -> dict[str, Any] | None:
        if refresh_token:
            email = self.decode_refresh_token(refresh_token)
            if email:
                access_token, expire_token = self.create_access_token(data={"sub": email})
                return {
                    "access_token": access_token,
                    "expire_token": expire_token,
                    "email": email,
            }
        return None


auth_service = Auth()
