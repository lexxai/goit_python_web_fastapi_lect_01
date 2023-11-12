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
