import logging
from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlalchemy.orm import Session


from src.database.db import get_db
from src.database.models import User
from src.repository import users as repository_users
from src.routes.auth.auth import get_current_user
from src.conf.config import settings
from src.shemas.users import UserDetailResponse, UserResponse
from src.services.cloudinary import Cloudinary

router = APIRouter(prefix="/users", tags=["users"])

logger = logging.getLogger(f"{settings.app_name}.{__name__}")


@router.get("/me/", response_model=UserResponse, response_model_exclude_none=True)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.patch("/avatar", response_model=UserResponse, response_model_exclude_unset=True)
async def update_avatar_user(
    file: UploadFile = File(), current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    public_id = Cloudinary.generate_public_id_by_email(str(current_user.email))
    r = Cloudinary.upload(file.file, public_id)
    src_url = Cloudinary.generate_url(r, public_id)
    user = await repository_users.update_avatar(current_user.email, src_url, db)  # type: ignore
    return user
