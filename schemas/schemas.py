from pydantic import BaseModel, Field

class UserSchema(BaseModel):
    name: str = Field(max_length=100)
    login: str = Field(max_length=50)
    password: str = Field(max_length=20)

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