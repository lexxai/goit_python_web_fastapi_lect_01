from sqlalchemy.orm import Session

from src.database.models import User


async def get_user_by_email(email: str, db: Session) -> User | None:
    try:
        return db.query(User).filter_by(email=email).first()
    except Exception:
        ...
    return None


async def get_user_by_name(username: str | None, db: Session) -> User | None:
    try:
        return db.query(User).filter_by(email=username).first()
    except Exception:
        ...
    return None


async def update_user_refresh_token(
    user: User, refresh_token: str | None, db: Session
) -> str | None:
    try:
        user.refresh_token = refresh_token
        db.commit()
        return refresh_token
    except Exception:
        ...
    return None

async def update_by_name_refresh_token(
    username: str | None, refresh_token: str | None, db: Session
) -> str | None:
    try:
        user = await get_user_by_name(username, db)
        if user is None:
            return None
        user.refresh_token = refresh_token
        db.commit()
        return refresh_token
    except Exception:
        ...
    return None
