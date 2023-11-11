from sqlalchemy.orm import Session
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    func,
    event,
)

from src.database.models import User

from src.auth.hash import Hash
from src.auth import auth_oauth2refresh as authLib

hash_handler = Hash()



async def get_user_by_name(username: str, db: Session):
    try:
        return db.query(User).filter(User.email == username).first()
    except Exception:
        ...
    return None


async def signup(username: str, password: str, db: Session):
    try:
        user = await get_user_by_name(username=username, db=db)
        if user:
            return None
        new_user = User(
            email=username, password=hash_handler.get_password_hash(password)
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception:
        ...
    return None


async def login(username: str, password: str, db: Session):
    user = await get_user_by_name(username=username, db=db)
    if user is None:
        return None
    if not hash_handler.verify_password(password, user.password):
        return None
    # Generate JWT
    access_token = await authLib.create_access_token(data={"sub": user.email})
    refresh_token = await authLib.create_refresh_token(data={"sub": user.email})
    token = {"access_token": access_token, "token_type": "bearer"}
    token.update({"refresh_token": refresh_token})
    return token


async def update_refresh_token(username: str, refresh_token: str, db: Session):
    user = await get_user_by_name(username=username, db=db)
    if user is None:
        return None
    user.refresh_token = Column(refresh_token)
    db.commit()
    return refresh_token
