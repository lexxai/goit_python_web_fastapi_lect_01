from sqlalchemy.orm import Session

from src.shemas import UserModel
from src.database.models import User
from src.auth.authSimple import Hash, create_access_token

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
    access_token = await create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}