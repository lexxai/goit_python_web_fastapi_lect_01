from sqlalchemy.orm import Session

from src.shemas import UserModel
from src.database.models import User
from src.conf.auth import AUTH_LIB

# AUTH_LIB can be Simple, OAuth2REfresh, OAuth2
if AUTH_LIB == "Simple":
    from src.auth import authSimple as authLib
if AUTH_LIB == "OAuth2REfresh":
    from src.auth import authOauth2Refresh as authLib
else:
    from src.auth import authOauth2 as authLib

hash_handler = authLib.Hash()

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
    if refresh_token:
        token.update({"refresh_token": refresh_token})
    return token
