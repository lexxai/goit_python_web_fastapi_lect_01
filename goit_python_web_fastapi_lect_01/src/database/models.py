import enum

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    func,
    event,
    Enum,
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Role(enum.Enum):
    admin: str = "admin"  # type: ignore
    moderator: str = "moderator"  # type: ignore
    user: str = "user"  # type: ignore


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username: str | Column[str] = Column(String(150), nullable=False)
    email: str | Column[str] = Column(String(150), nullable=False, unique=True)
    password: str | Column[str] = Column(String(255), nullable=False)
    refresh_token: str | Column[str] | None = Column(String(255), nullable=True)
    avatar: str | Column[str] | None = Column(String(255), nullable=True)
    role: Enum | Column[Enum] = Column("roles", Enum(Role), default=Role.user)


class Owner(Base):
    __tablename__ = "owners"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class Cat(Base):
    __tablename__ = "cats"

    id = Column(Integer, primary_key=True, index=True)
    nickname: str | Column[str] = Column(String)
    age: int | Column[int] = Column(Integer)
    description: str | Column[str] = Column(String)
    vaccinated: bool | Column[bool] = Column(Boolean, default=False)
    owner_id: int | Column[int] | None = Column(
        Integer, ForeignKey("owners.id"), nullable=True
    )
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    owner = relationship("Owner", backref="cats")


@event.listens_for(Cat, "before_insert")
@event.listens_for(Cat, "before_update")
def updated_vacinated_bu(mapper, conn, target):
    if target.nickname == "Mur":
        target.vaccinated = True
