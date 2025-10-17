from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    login: str = Field(min_length=3, max_length=32)
    password: str = Field(min_length=8, max_length=128)

class UserUpdate(BaseModel):
    email: Optional[EmailStr]
    login: Optional[str] = Field(min_length=3, max_length=32)

class UserPasswordChange(BaseModel):
    password: str = Field(min_length=8, max_length=128)

class UserPublic(BaseModel):
    id: int
    email: EmailStr
    login: str
    createdAt: datetime
    updatedAt: datetime

# class UserSchema(BaseModel):
#     name: str = Field(max_length=100)
#     login: str = Field(max_length=50)
#     password: str = Field(max_length=20)

class ThoughtSchema(BaseModel):
    id: int
    user_id: int
    stage: int
    capture: str
    date: str

class ThoughtUpdSchema(BaseModel):
    id: int
    user_id: int | None = None
    stage: int
    capture: str | None = None
    date: str | None = None