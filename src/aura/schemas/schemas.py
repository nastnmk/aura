from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    name: str = Field(min_length=3, max_length=32)
    login: str = Field(min_length=3, max_length=32)
    password: str = Field(min_length=8, max_length=128)

class UserUpdate(BaseModel):
    email: Optional[EmailStr]
    name: str = Field(min_length=3, max_length=32)
    login: Optional[str] = Field(min_length=3, max_length=32)

class UserPasswordChange(BaseModel):
    new_password: str = Field(min_length=8, max_length=128)

class UserPublic(BaseModel):
    id: int
    email: EmailStr
    login: str
    createdat: datetime
    updatedat: datetime

class ThoughtSchema(BaseModel):
    user_id: int

class StageSchema(BaseModel):
    thought_id: int
    stage: int
    capture: str

class StageUpdSchema(BaseModel):
    id: int
    capture: str | None = None