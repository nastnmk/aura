from models.models import Base
from repositories.settings import engine
from fastapi import APIRouter

router = APIRouter(prefix="/settings", tags=["settings"])  # протягиваем роутеры, чтобы в основном файле не лепить все ручки

@router.post("/setup_db")
async def setup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)     # очистка бд и создание новых экземпляров
        await conn.run_sync(Base.metadata.create_all)
    return {"status": "created"}