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
from src.shemas.users import UserModel

from src.repository import auth_oauth2refresh as repository_auth
from src.auth import auth_oauth2refresh as authLib


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
@router.post("/login", response_model=AccessTokenResponse, response_model_exclude_unset=True)
async def login(
    body: Annotated[authLib.auth_response_model, Depends()],
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


@router.get("/secret")
async def read_item(current_user: User = Depends(authLib.get_current_user)):
    return {"message": "secret router", "owner": current_user.email}


@router.get("/refresh_token")
async def refresh_token(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    token: str = credentials.credentials
    email = await authLib.get_email_form_refresh_token(token)
    user = db.query(User).filter(User.email == email).first()
    if user.refresh_token != token: # type: ignore
        user.refresh_token = None   # type: ignore
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )

    access_token = await authLib.create_access_token(data={"sub": email})
    refresh_token = await authLib.create_refresh_token(data={"sub": email})
    user.refresh_token = refresh_token # type: ignore
    db.commit()
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        }
