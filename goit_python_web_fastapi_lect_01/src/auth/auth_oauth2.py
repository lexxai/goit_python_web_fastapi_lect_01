from datetime import datetime, timedelta
from os import environ
import pathlib
import sys

from typing import Optional

from fastapi import Depends, HTTPException
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer  # Bearer .....
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from starlette import status

try:
    from src.database.db import get_db
    from src.database.models import User
    from src.shemas.users import UserModel, AccessTokenRefreshResponse, AccessTokenResponse
except ImportError:
    sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))
    from database.db import get_db
    from database.models import User
    from shemas.users import UserModel, AccessTokenRefreshResponse, AccessTokenResponse


class Hash:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str):
        return self.pwd_context.hash(password)


SECRET_KEY = environ.get("TOKEN_SECRET_KEY")
assert SECRET_KEY, "MISSED TOKEN SECRET_KEY"

ALGORITHM = "HS512"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

auth_response_model = OAuth2PasswordRequestForm
auth_answer_model = AccessTokenResponse


# define a function to generate a new access token
async def create_access_token(data: dict, expires_delta: Optional[float] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + timedelta(seconds=expires_delta)
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload["sub"]
        if email is None:
            raise credentials_exception
    except JWTError as e:
        raise credentials_exception

    user: User = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user


# EMPTY INTERFACE
async def get_email_form_refresh_token(refresh_token: str) -> str | None:
    return None


async def create_refresh_token(
    data: dict, expires_delta: Optional[float] = None
) -> str | None:
    return None


# print("Auth OAuth2 Lib")
