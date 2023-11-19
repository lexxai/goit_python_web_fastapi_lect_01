import pickle
from sqlalchemy.orm import Session
import redis as redis

# from fastapi import Depends
from src.conf.config import settings
from src.database.models import User
from src.services.auth.auth import auth_service
from src.repository import users as repository_users

# from src.database.db import get_db


# auth_service = Auth()

redis_conn = redis.Redis(host=settings.redis_host, port=int(settings.redis_port), db=0)


async def a_get_current_user(token: str | None, db: Session) -> User | None:
    if not token:
        return None
    email = auth_service.decode_jwt(token)
    if email is None:
        return None
    try:
        user = redis_conn.get(f"user:{email}")
    except Exception as err:
        print("Error Redis read", err)
        user = None
    if user is None:
        user = await repository_users.get_user_by_email(email, db)
        if user:
            try:
                redis_conn.set(f"user:{email}", pickle.dumps(user))
                redis_conn.expire(f"user:{email}", 900)
                print("Save to Redis", str(user.email))
            except Exception as err:
                print("Error redis save", err)
    else:
        user = pickle.loads(user)  # type: ignore
        print("Get from Redis", str(user.email))

    return user


async def signup(body, db: Session):
    try:
        user = await repository_users.get_user_by_name(body.username, db)
        if user is not None:
            return None
        body.password = auth_service.get_password_hash(body.password)
        # if not body.email:
        #     body.email = body.username
        new_user = await repository_users.create_user(body, db)
    except Exception:
        return None
    return new_user


def login(user: User, password: str, db: Session):
    if user is None:
        return None
    if not auth_service.verify_password(password, user.password):
        return None
    # Generate JWT
    access_token, expire_token = auth_service.create_access_token(data={"sub": user.email})
    token = {"access_token": access_token, "token_type": "bearer", "expire_access_token": expire_token}
    refresh_token, expire_token = auth_service.create_refresh_token(data={"sub": user.email})
    token.update({"refresh_token": refresh_token, "expire_refresh_token": expire_token})
    return token


async def update_refresh_token(username: str, refresh_token: str, db: Session):
    return await repository_users.update_by_name_refresh_token(username, refresh_token, db)
