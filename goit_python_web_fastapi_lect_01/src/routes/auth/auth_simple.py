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

from src.shemas.users import NewUserResponse, AccessTokenResponse
from src.shemas.users import UserModel

from src.repository.auth import auth_simple as repository_auth
from src.auth import auth_simple as authLib


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
@router.post("/login", response_model=AccessTokenResponse)
async def login(
    body: Annotated[UserModel, Depends()],
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
    return token


@router.get("/secret")
async def read_item(current_user: User = Depends(authLib.get_current_user)):
    return {"message": "secret router", "owner": current_user.email}

