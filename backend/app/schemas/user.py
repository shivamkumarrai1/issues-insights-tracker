from pydantic import BaseModel, EmailStr
from enum import Enum

class RoleEnum(str, Enum):
    ADMIN = "ADMIN"
    MAINTAINER = "MAINTAINER"
    REPORTER = "REPORTER"

class UserBase(BaseModel):
    email: EmailStr
    role: RoleEnum

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: str
    role: RoleEnum
