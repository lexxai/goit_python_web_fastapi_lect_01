from typing import List

from fastapi import APIRouter, Path, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.shemas import CatModel, CatResponse, CatVactinatedModel
from src.database.models import Cat
from src.repository import cats as repository_cats

"""
CATS
"""

router = APIRouter(prefix="/cats", tags=["cats"])


@router.get("", response_model=List[CatResponse])
async def get_cats(limit: int = 10, offset: int = 0, db: Session = Depends(get_db)):
    cats = await repository_cats.get_cats(limit, offset, db)
    return cats


@router.get("/{cat_id}", response_model=CatResponse)
async def get_cat(cat_id: int = Path(ge=1), db: Session = Depends(get_db)):
    cat = await repository_cats.get_cat_by_id(cat_id, db)
    if cat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return cat


@router.post("", response_model=CatResponse, status_code=status.HTTP_201_CREATED)
async def create_cat(body: CatModel, db: Session = Depends(get_db)):
    cat = await repository_cats.create(body, db)
    if cat is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Owner not exist!"
        )
    return cat


@router.put("/{cat_id}", response_model=CatResponse)
async def update_cat(
    body: CatModel, cat_id: int = Path(ge=1), db: Session = Depends(get_db)
):
    cat = db.query(Cat).filter_by(id=cat_id).first()
    if cat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    owner = db.query(Owner).filter_by(id=body.owner_id).first()
    if owner is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Owner not exist!"
        )
    cat.nickname = body.nickname
    cat.age = body.age
    cat.description = body.description
    cat.vaccinated = body.vaccinated
    cat.nickname = body.nickname
    cat.owner_id = body.owner_id
    db.commit()
    return cat


@router.patch(
    "/{cat_id}/vactinated",
    response_model=CatResponse,
)
async def vactinated_cat(
    body: CatVactinatedModel, cat_id: int = Path(ge=1), db: Session = Depends(get_db)
):
    cat = db.query(Cat).filter_by(id=cat_id).first()
    if cat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    if cat.vaccinated != body.vaccinated:
        cat.vaccinated = body.vaccinated
        db.commit()
        return cat
    else:
        raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED, detail="")


@router.delete("/{cat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_cat(cat_id: int = Path(ge=1), db: Session = Depends(get_db)):
    cat = db.query(Cat).filter_by(id=cat_id).first()
    if cat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    db.delete(cat)
    db.commit()
    return None
