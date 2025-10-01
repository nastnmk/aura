from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import Annotated
from fastapi import  Depends


engine = create_async_engine("sqlite+aiosqlite:///data.db")
session = async_sessionmaker(engine, expire_on_commit=False)

async def get_session():
    async with session() as new_session:
        yield new_session


SessionDep = Annotated[AsyncSession, Depends(get_session)]

