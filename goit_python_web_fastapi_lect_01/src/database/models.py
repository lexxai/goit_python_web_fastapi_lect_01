from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, func, event
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Owner(Base):
    __tablename__ = "owners"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class Cat(Base):
    __tablename__ = "cats"

    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String)
    age = Column(Integer)
    description = Column(String)
    vaccinated = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("owners.id"), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    owner = relationship("Owner", backref="cats")


@event.listens_for(Cat, "before_insert")
def updated_vacinated(mapper, conn, target):
    if target.nickname == "Mur":
        target.vaccinated = True
        

@event.listens_for(Cat, "before_update")
def updated_vacinated(mapper, conn, target):
    if target.nickname == "Mur":
        target.vaccinated = True
