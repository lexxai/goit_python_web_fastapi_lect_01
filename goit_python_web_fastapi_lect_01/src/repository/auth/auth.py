from sqlalchemy.orm import Session
#from fastapi import Depends

from src.database.models import User
from src.services.auth.auth import Auth
from src.repository import users as repository_users
#from src.database.db import get_db



auth_service = Auth()


async def a_get_current_user(token: str, db: Session) -> User | None:
    email = auth_service.decode_jwt(token)
    if email is None:
        return None
    user = await repository_users.get_user_by_email(email, db)
    return user


async def signup(username: str, password: str, db: Session):
    try:
        user = await repository_users.get_user_by_name(username, db)
        if user:
            return None
        new_user = User(
            email=username, password=auth_service.get_password_hash(password)
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception:
        ...
    return None


async def login(username: str, password: str, db: Session):
    user = await repository_users.get_user_by_name(username, db)
    if user is None:
        return None
    if not auth_service.verify_password(password, user.password):
        return None
    # Generate JWT
    access_token = await auth_service.create_access_token(data={"sub": user.email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": user.email})
    token = {"access_token": access_token, "token_type": "bearer"}
    token.update({"refresh_token": refresh_token})
    return token


async def update_refresh_token(username: str, refresh_token: str, db: Session):
    user = await repository_users.get_user_by_name(username, db)
    if user is None:
        return None
    user.refresh_token = refresh_token
    db.commit()
    return refresh_token
