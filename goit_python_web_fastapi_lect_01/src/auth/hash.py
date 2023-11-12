from datetime import datetime, timedelta
from os import environ
from typing import Optional

from fastapi import Depends, HTTPException
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from starlette import status

from src.database.db import get_db



class Hash:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    SECRET_KEY: str
    ALGORITHM: str

    def __init__(self, init_key: str | None = None, init_algorithm: str = "HS512") -> None:
        self.SECRET_KEY: str = init_key if init_key else environ.get("TOKEN_SECRET_KEY", "") 
        assert self.SECRET_KEY, "MISSED TOKEN SECRET_KEY"
        self.ALGORITHM = init_algorithm
        assert self.ALGORITHM, "MISSED ALGORITHM"

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str):
        return self.pwd_context.hash(password)

    # define a function to generate a new access token
    async def create_access_token(
        self, data: dict, expires_delta: Optional[float] = None
    ):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update(
            {"iat": datetime.utcnow(), "exp": expire, "scope": "access_token"}
        )
        encoded_access_token = jwt.encode(
            to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM
        )
        return encoded_access_token


