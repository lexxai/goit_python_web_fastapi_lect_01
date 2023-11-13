from pydantic import BaseModel, Field, EmailStr


from src.database.models import Role


class AccessTokenRefreshResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: str


class AccessTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserModel(BaseModel):
    username: str = Field(min_length=2, max_length=150)
    email: EmailStr
    password: str = Field(min_length=6, max_length=32)


class NewUserResponse(BaseModel):
    username: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    avatar: str | None
    role: Role

    class Config:
        from_attributes = True
