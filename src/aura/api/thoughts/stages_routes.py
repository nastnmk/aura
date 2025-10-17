from fastapi import APIRouter
from sqlalchemy import select
from aura.repositories.settings import SessionDep
from aura.models.models import StageModel
from aura.schemas.schemas import StageSchema, StageUpdSchema  # если нужны

router = APIRouter(prefix="/stages", tags=["stages"])

@router.get("/")
async def list_stages(new_session: SessionDep):
    result = await new_session.execute(select(StageModel))
    return result.scalars().all()

