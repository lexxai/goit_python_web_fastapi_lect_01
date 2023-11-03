from pydantic import BaseModel, Field, EmailStr


class OwnerModel(BaseModel):
    email: EmailStr
    # email: str = Field(default="email@examole.com", pattern=r'^\w+@\w+\.\w+$')


class OwnerResponse(BaseModel):
    id: int = 1
    email: EmailStr

    class Config:
        from_attributes = True

