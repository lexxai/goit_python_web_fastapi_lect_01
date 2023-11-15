from typing import Annotated, Any, List
from fastapi import APIRouter, Depends, HTTPException, Request, Response, Security, status, Cookie, BackgroundTasks
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBasicCredentials,
    HTTPBearer,
)
from sqlalchemy.orm import Session
from src.services.emails import send_email

from src.database.db import get_db
from src.database.models import User
from src.shemas.users import UserDetailResponse, UserModel
from src.repository.auth import auth as repository_auth
from src.services.auth.auth import auth_service, Auth
from src.repository import users as repository_users
from src.shemas.auth import RequestEmail

router = APIRouter(prefix="", tags=["Auth"])

security = HTTPBearer()

SET_COOKIES = False


@router.post(
    "/signup",
    response_model=UserDetailResponse,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
)
async def signup(body: UserModel, background_tasks: BackgroundTasks, request: Request, db: Session = Depends(get_db)):
    new_user = await repository_auth.signup(body=body, db=db)
    if new_user is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account already exists")
    background_tasks.add_task(send_email, str(new_user.email), str(new_user.username), str(request.base_url))
    return {"user": new_user, "detail": "User successfully created. Check your email for confirmation."}


# Annotated[OAuth2PasswordRequestForm, Depends()]
# auth_response_model = Depends()
@router.post("/login", response_model=auth_service.token_response_model)
async def login(
    response: Response,
    body: Annotated[auth_service.auth_response_model, Depends()],  # type: ignore
    db: Session = Depends(get_db),
):
    user = await repository_users.get_user_by_email(body.username, db)
    if user is None:
        exception_data = {
            "status_code": status.HTTP_401_UNAUTHORIZED,
            "detail": "Invalid credentianal",
        }
        raise HTTPException(**exception_data)
    if not bool(user.confirmed):
        exception_data = {
            "status_code": status.HTTP_401_UNAUTHORIZED,
            "detail": "Not confirmed",
        }
        raise HTTPException(**exception_data)

    token = repository_auth.login(user=user, password=body.password, db=db)
    if token is None:
        exception_data = {
            "status_code": status.HTTP_401_UNAUTHORIZED,
            "detail": "Invalid credentianal",
        }
        if SET_COOKIES:
            response.delete_cookie(key="access_token", httponly=True, path="/api/")
            exception_data.update(
                {
                    "headers": {
                        "set-cookie": response.headers.get("set-cookie", ""),
                    }
                }
            )
        raise HTTPException(**exception_data)
    refresh_token = token.get("refresh_token")
    if refresh_token:
        await repository_auth.update_refresh_token(username=body.username, refresh_token=refresh_token, db=db)
    new_access_token = token.get("access_token")
    if SET_COOKIES:
        if new_access_token:
            response.set_cookie(
                key="access_token",
                value=new_access_token,
                httponly=True,
                path="/api/",
                expires=token.get("expire_access_token"),
            )
        else:
            response.delete_cookie(key="access_token", httponly=True, path="/api/")
        if new_access_token and refresh_token:
            print(f"{token.get('expire_refresh_token')=}")
            response.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                path="/api/",
                expires=token.get("expire_refresh_token"),
            )
        else:
            response.delete_cookie(key="refresh_token", httponly=True, path="/api/")
    print("login", token)
    return token


async def get_current_user(
    response: Response,
    access_token: Annotated[str | None, Cookie()] = None,
    refresh_token: Annotated[str | None, Cookie()] = None,
    token: str | None = Depends(auth_service.auth_scheme),
    db: Session = Depends(get_db),
) -> User | None:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": "Bearer",
            "set-cookie": response.headers.get("set-cookie", ""),
        },
    )
    user = None
    new_access_token = None
    print(f"{access_token=}, {refresh_token=}, {token=}")
    if not token:
        print("used cookie access_token")
        token = access_token
    if token:
        user = await repository_auth.a_get_current_user(token, db)
        if not user and token != access_token:
            user = await repository_auth.a_get_current_user(access_token, db)
        if not user and refresh_token:
            result = auth_service.refresh_access_token(refresh_token)
            print(f"refresh_access_token  {result=}")
            if result:
                new_access_token = result.get("access_token")
                email = result.get("email")
                user = await repository_users.get_user_by_email(str(email), db)
                if SET_COOKIES:
                    if new_access_token:
                        response.set_cookie(
                            key="access_token",
                            value=new_access_token,
                            httponly=True,
                            path="/api/",
                            expires=result.get("expire_token"),
                        )
                    else:
                        response.delete_cookie(key="access_token", httponly=True, path="/api/")
    if user is None:
        raise credentials_exception
    return user


async def get_current_user_dbtoken(
    response: Response,
    access_token: Annotated[str | None, Cookie()] = None,
    refresh_token: Annotated[str | None, Cookie()] = None,
    token: str | None = Depends(auth_service.auth_scheme),
    db: Session = Depends(get_db),
) -> User | None:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": "Bearer",
            "set-cookie": response.headers["set-cookie"],
        },
    )
    user = None
    new_access_token = None
    print(f"{access_token=}, {refresh_token=}")
    if not token:
        token = access_token
    if token:
        user = await repository_auth.a_get_current_user(token, db)
        if not user and refresh_token:
            email = auth_service.decode_refresh_token(refresh_token)
            user = await repository_users.get_user_by_email(str(email), db)
            # print(f"refresh_access_token {email=} {user.email} {user.refresh_token}")  # type: ignore
            if refresh_token == user.refresh_token:  # type: ignore
                result = auth_service.refresh_access_token(refresh_token)
                print(f"refresh_access_token  {result=}")
                if result:
                    new_access_token = result.get("access_token")
                    email = result.get("email")
                    user = await repository_users.get_user_by_email(str(email), db)
                    if SET_COOKIES:
                        if new_access_token:
                            response.set_cookie(
                                key="access_token",
                                value=new_access_token,
                                httponly=True,
                                path="/api/",
                                expires=result.get("expire_token"),
                            )
                        else:
                            response.delete_cookie(key="access_token", httponly=True, path="/api/")
            else:
                await repository_users.update_user_refresh_token(user, "", db)
                response.delete_cookie(key="refresh_token", httponly=True, path="/api/")
                user = None
    if user is None:
        raise credentials_exception
    return user


@router.get("/secret")
async def read_item(current_user: User = Depends(get_current_user)):
    auth_result = {"email": current_user.email}
    return {"message": "secret router", "owner": auth_result}


@router.get("/secret_dbtoken")
async def read_item_dbtoken(current_user: User = Depends(get_current_user_dbtoken)):
    auth_result = {"email": current_user.email}
    return {"message": "secret router", "owner": auth_result}


@router.get("/refresh_token")
async def refresh_token(
    response: Response,
    refresh_token: Annotated[str | None, Cookie()] = None,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    token: str = credentials.credentials
    print(f"refresh_token {token=}")
    if not token and refresh_token:
        token = refresh_token
    email = auth_service.decode_refresh_token(token)
    print(f"refresh_token {email=}")
    user: User | None = await repository_users.get_user_by_email(email, db)
    if user and user.refresh_token != token:  # type: ignore
        await repository_users.update_user_refresh_token(user, None, db)
        response.delete_cookie(key="refresh_token", httponly=True, path="/api/")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={
                "set-cookie": response.headers.get("set-cookie", ""),
            },
        )
    new_access_token, expire_access_token = auth_service.create_access_token(data={"sub": email})
    new_refresh_token, expire_refresh_token = auth_service.create_refresh_token(data={"sub": email})
    await repository_users.update_user_refresh_token(user, new_refresh_token, db)
    if SET_COOKIES:
        if new_access_token:
            response.set_cookie(
                key="access_token",
                value=new_access_token,
                httponly=True,
                path="/api/",
                expires=expire_access_token,
            )
        else:
            response.delete_cookie(key="access_token", httponly=True, path="/api/")
        if new_access_token:
            response.set_cookie(
                key="refresh_token",
                value=new_refresh_token,
                httponly=True,
                path="/api/",
                expires=expire_refresh_token,
            )
        else:
            response.delete_cookie(key="refresh_token", httponly=True, path="/api/")
    return {
        "access_token": new_access_token,
        "expire_access_token": expire_access_token,
        "refresh_token": new_refresh_token,
        "expire_refresh_token": expire_refresh_token,
        "token_type": "bearer",
    }


@router.get("/confirmed_email/{token}")
async def confirmed_email(token: str, db: Session = Depends(get_db)):
    email = auth_service.get_email_from_token(token)
    if email:
        user = await repository_users.get_user_by_email(email, db)
        if user:
            if bool(user.confirmed):
                return {"message": "Your email is already confirmed"}
            await repository_users.confirmed_email(email, db)
            return {"message": "Email confirmed"}
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error")


@router.post('/request_email')
async def request_email(body: RequestEmail, background_tasks: BackgroundTasks, request: Request,
                        db: Session = Depends(get_db)):
    user = await repository_users.get_user_by_email(body.email, db)
    if user:
        if bool(user.confirmed):
                return {"message": "Your email is already confirmed"}
        background_tasks.add_task(send_email, str(user.email), str(user.username), str(request.base_url))
    return {"message": "Check your email for confirmation."}
