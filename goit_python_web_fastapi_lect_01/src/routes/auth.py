from typing import Annotated, List

from fastapi import APIRouter, Path, Depends, HTTPException, status
from fastapi.security import HTTPBasicCredentials
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User

from src.shemas import AccessTokenResponse, NewUserResponse
from src.repository import authLib as repository_auth
from src.shemas import UserModel

from src.repository.authLib import get_current_user, auth_response_model


router = APIRouter(prefix="", tags=["Auth"])


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
async def login(body: Annotated[auth_response_model,Depends()], db: Session = Depends(get_db)):
    token = await repository_auth.login(
        username=body.username, password=body.password, db=db
    )
    print(f"login . token=")
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentianal",
        )
    return token


@router.get("/secret")
async def read_item(current_user: User = Depends(get_current_user)):
    return {"message": "secret router", "owner": current_user.email}
