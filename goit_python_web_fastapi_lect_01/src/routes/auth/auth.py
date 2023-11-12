from typing import Annotated, List

from fastapi import APIRouter, Path, Depends, HTTPException, Security, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBasicCredentials,
    HTTPBearer,
)
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User

from src.shemas.users import AccessTokenResponse, NewUserResponse

from src.repository.auth import auth as repository_auth
from src.repository import users as repository_users

router = APIRouter(prefix="", tags=["Auth"])

security = HTTPBearer()


@router.post(
    "/signup", response_model=NewUserResponse, status_code=status.HTTP_201_CREATED
)
async def signup(body: HTTPBasicCredentials, db: Session = Depends(get_db)):
    new_user = await repository_auth.signup(
        username=body.username, password=body.password, db=db
    )
    if new_user is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Account already exists"
        )
    return {"username": new_user.email}


# Annotated[OAuth2PasswordRequestForm, Depends()]
# auth_response_model = Depends()
@router.post("/login", response_model=repository_auth.auth_service.token_response_model)
async def login(
    body: Annotated[repository_auth.auth_service.auth_response_model, Depends()],
    db: Session = Depends(get_db),
):
    token = await repository_auth.login(
        username=body.username, password=body.password, db=db
    )
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentianal",
        )
    refresh_token = token.get("refresh_token")
    if refresh_token:
        await repository_auth.update_refresh_token(
            username=body.username, refresh_token=refresh_token, db=db
        )
    return token


async def get_current_user(
    token: str = Depends(repository_auth.auth_service.auth_scheme), db: Session = Depends(get_db)
) -> User | None:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user = await repository_auth.a_get_current_user(token, db)
    if user is None:
        raise credentials_exception
    return user


@router.get("/secret")
async def read_item(current_user: User = Depends(get_current_user)):
    return {"message": "secret router", "owner": current_user.email}


@router.get("/refresh_token")
async def refresh_token(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    token: str = credentials.credentials
    email = await repository_auth.auth_service.decode_refresh_token(token)
    user: User | None = await repository_users.get_user_by_email(email,db)
    if user and user.refresh_token != token:  # type: ignore
            await repository_users.update_user_refresh_token(user,"", db)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
            )

    access_token = await repository_auth.auth_service.create_access_token(data={"sub": email})
    refresh_token = await repository_auth.auth_service.create_refresh_token(data={"sub": email})
    await repository_users.update_user_refresh_token(user, refresh_token, db)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        }
