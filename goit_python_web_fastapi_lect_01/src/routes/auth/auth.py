from typing import Annotated, Any, List

from fastapi import APIRouter, Path, Depends, HTTPException, Security, status, Cookie
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBasicCredentials,
    HTTPBearer,
)

from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User

from src.shemas.users import AccessTokenResponse, UserResponse, UserModel

from src.repository.auth import auth as repository_auth
from src.repository import users as repository_users


router = APIRouter(prefix="", tags=["Auth"])

security = HTTPBearer()


@router.post(
    "/signup",
    response_model=UserResponse,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
)
async def signup(body: UserModel, db: Session = Depends(get_db)):
    new_user = await repository_auth.signup(body=body, db=db)
    if new_user is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Account already exists"
        )
    return new_user


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
    access_token: Annotated[str | None, Cookie()] = None,
    refresh_token: Annotated[str | None, Cookie()] = None,
    token: str | None = Depends(repository_auth.auth_service.auth_scheme),
    db: Session = Depends(get_db),
) -> dict | None:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user = None
    new_access_token = None
    print(f"{access_token=}, {refresh_token=}")
    if not token:
        token = access_token
    if token:
        user = await repository_auth.a_get_current_user(token, db)
        if not user and refresh_token:
            result = await refresh_access_token(refresh_token)
            print(f"refresh_access_token  {result=}")
            if result:
                new_access_token = result.get("access_token")
                email = result.get("email")
                user = await repository_users.get_user_by_email(str(email), db)
    if user is None:
        raise credentials_exception
    auth_result: dict[str, User | str] = {"user": user}
    if new_access_token:
        auth_result.update({"new_access_token": new_access_token})

    return auth_result


async def get_current_user_dbtoken(
    access_token: Annotated[str | None, Cookie()] = None,
    refresh_token: Annotated[str | None, Cookie()] = None,
    token: str | None = Depends(repository_auth.auth_service.auth_scheme),
    db: Session = Depends(get_db),
) -> dict | None:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user = None
    new_access_token = None
    print(f"{access_token=}, {refresh_token=}")
    if not token:
        token = access_token
    if token:
        user = await repository_auth.a_get_current_user(token, db)
        if not user and refresh_token:
            email = await repository_auth.auth_service.decode_refresh_token(
                refresh_token
            )
            user = await repository_users.get_user_by_email(str(email), db)
            print(f"refresh_access_token {email=} {user.email} {user.refresh_token}")  # type: ignore
            if refresh_token == user.refresh_token:  # type: ignore
                result = await refresh_access_token(refresh_token)
                print(f"refresh_access_token  {result=}")
                if result:
                    new_access_token = result.get("access_token")
                    email = result.get("email")
                    user = await repository_users.get_user_by_email(str(email), db)
            else:
                await repository_users.update_user_refresh_token(user, "", db)
                user = None
    if user is None:
        raise credentials_exception
    auth_result: dict[str, User | str] = {"user": user}
    if new_access_token:
        auth_result.update({"new_access_token": new_access_token})

    return auth_result


@router.get("/secret")
async def read_item(current_user: User = Depends(get_current_user)):
    auth_result = {"email": current_user.get("user").email}
    if current_user.get("new_access_token"):
        auth_result.update({"new_access_token": current_user.get("new_access_token")})
    return {"message": "secret router", "owner": auth_result}


@router.get("/secret_dbtoken")
async def read_item_dbtoken(current_user: User = Depends(get_current_user_dbtoken)):
    auth_result = {"email": current_user.get("user").email}
    if current_user.get("new_access_token"):
        auth_result.update({"new_access_token": current_user.get("new_access_token")})
    return {"message": "secret router", "owner": auth_result}


async def refresh_access_token(refresh_token: str) -> dict[str, str] | None:
    if refresh_token:
        email = await repository_auth.auth_service.decode_refresh_token(refresh_token)
        if email:
            access_token = await repository_auth.auth_service.create_access_token(
                data={"sub": email}
            )
            return {"access_token": access_token, "email": email}
    return None


@router.get("/refresh_token")
async def refresh_token(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    token: str = credentials.credentials
    email = await repository_auth.auth_service.decode_refresh_token(token)
    user: User | None = await repository_users.get_user_by_email(email, db)
    if user and user.refresh_token != token:  # type: ignore
        await repository_users.update_user_refresh_token(user, "", db)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )

    access_token = await repository_auth.auth_service.create_access_token(
        data={"sub": email}
    )
    refresh_token = await repository_auth.auth_service.create_refresh_token(
        data={"sub": email}
    )
    await repository_users.update_user_refresh_token(user, refresh_token, db)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }
