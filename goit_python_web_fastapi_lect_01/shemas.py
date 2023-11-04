from pydantic import BaseModel, Field, EmailStr


class OwnerModel(BaseModel):
    email: EmailStr
    # email: str = Field(default="email@examole.com", pattern=r'^\w+@\w+\.\w+$')


class OwnerResponse(BaseModel):
    id: int = 1
    email: EmailStr

    class Config:
        from_attributes = True


class CatModel(BaseModel):
    nickname: str = Field("Lukas", min_length=3, max_length=16 )
    age: int = Field(1, ge=0, le=30)
    description: str
    vaccinated : bool = False
    owner_id: int = Field(1, gt=0)


class CatResponse(BaseModel):
    id: int 
    nickname: str
    age: int
    description: str
    vaccinated : bool 
    owner_id: OwnerResponse
    
    class Config:
        from_attributes = True