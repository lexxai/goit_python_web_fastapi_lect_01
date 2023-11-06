from sqlalchemy.orm import Session

from src.shemas import CatModel, CatVactinatedModel
from src.database.models import Cat


async def get_cats(limit: int, offset: int, db: Session):
    cats = db.query(Cat).limit(limit).offset(offset).all()
    return cats


async def get_cat_by_id(cat_id: int, db: Session):
    cat = db.query(Cat).filter_by(id=cat_id).first()
    return cat


async def get_cat_by_email(email: str, db: Session):
    cat = db.query(Cat).filter_by(email=email).first()
    return cat


async def create(body: CatModel, db: Session):
    cat = Cat(**body.model_dump())
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat


async def update(cat_id: int, body: CatModel, db: Session):
    cat = await get_cat_by_id(cat_id, db)
    if cat:
        cat.email = body.email
        db.commit()
    return cat


async def delete(cat_id: int, db: Session):
    cat = await get_cat_by_id(cat_id, db)
    if cat:
        db.delete(cat)
        db.commit()
    return cat
