from typing import List

from fastapi import APIRouter, Path, Depends, HTTPException, status
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session


from src.database.models import User, Role
from src.database.db import get_db
from src.shemas.cat import CatModel, CatVactinatedModel, CatResponse
from src.repository import cats as repository_cats
from src.repository import owners as repository_owners
from src.routes.auth import auth
from src.services.roles import RoleAccess

router = APIRouter(prefix="/cats", tags=["cats"])

allowed_operations_get = RoleAccess([Role.admin, Role.moderator, Role.user])
allowed_operations_create = RoleAccess([Role.admin, Role.moderator, Role.user])
allowed_operations_update = RoleAccess([Role.admin, Role.moderator])
allowed_operations_remove = RoleAccess([Role.admin])


@router.get(
    "",
    response_model=List[CatResponse],
    dependencies=[Depends(allowed_operations_get), Depends(RateLimiter(times=2, seconds=5))],
)
async def get_cats(
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth.get_current_user),
):
    cats = await repository_cats.get_cats(limit, offset, db)
    return cats


@router.get("/{cat_id}", response_model=CatResponse, dependencies=[Depends(allowed_operations_get)])
async def get_cat(
    cat_id: int = Path(ge=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(auth.get_current_user),
):
    cat = await repository_cats.get_cat_by_id(cat_id, db)
    if cat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return cat


@router.post(
    "",
    response_model=CatResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(allowed_operations_create)],
)
async def create_cat(
    body: CatModel,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth.get_current_user),
):
    owner = await repository_owners.get_owner_by_id(body.owner_id, db)
    if owner is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found owner")
    cat = await repository_cats.create(body, db)
    if cat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not created ")
    return cat


@router.put(
    "/{cat_id}",
    response_model=CatResponse,
    dependencies=[Depends(allowed_operations_update)],
    description="Only moderators and admin",
)
async def update_cat(
    body: CatModel,
    cat_id: int = Path(ge=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(auth.get_current_user),
):
    owner = await repository_owners.get_owner_by_id(body.owner_id, db)
    if owner is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found owner")
    cat = await repository_cats.update(cat_id, body, db)
    if cat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return cat


@router.patch(
    "/{cat_id}/vactinated",
    response_model=CatResponse,
    dependencies=[Depends(allowed_operations_update)],
    description="Only moderators and admin",
)
async def vactinated_cat(
    body: CatVactinatedModel,
    cat_id: int = Path(ge=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(auth.get_current_user),
):
    cat = await repository_cats.set_vactinated(cat_id, body, db)
    if cat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return cat


@router.delete(
    "/{cat_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(allowed_operations_remove)],
    description="Only admin",
)
async def remove_cat(
    cat_id: int = Path(ge=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(auth.get_current_user),
):
    cat = await repository_cats.delete(cat_id, db)
    if cat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return None
