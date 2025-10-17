from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import Annotated
from fastapi import Depends
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()

engine = create_async_engine(settings.DATABASE_URL, echo=False, pool_pre_ping=True)
session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def get_session():
    async with session() as new_session:
        yield new_session


SessionDep = Annotated[AsyncSession, Depends(get_session)]

