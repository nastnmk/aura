from fastapi import APIRouter
from sqlalchemy import select
from aura.schemas.schemas import ThoughtSchema
from aura.models.models import ThoughtModel
from aura.repositories.settings import SessionDep

router = APIRouter(prefix="/thoughts", tags=["thoughts"])

@router.get("/")
async def get(new_session: SessionDep):
    result = await new_session.execute(select(ThoughtModel))
    return result.scalars().all()

@router.post("/")
async def create(thought: ThoughtSchema, new_session: SessionDep):
    new_thought = ThoughtModel(user_id=thought.user_id)
    new_session.add(new_thought)
    await new_session.commit()
    return {"status": "OK"}

@router.delete("/")
async def delete(thought_id: int, new_session: SessionDep):
    result = await new_session.execute(
        select(ThoughtModel).where(ThoughtModel.id == thought_id)
    )
    for obj in result.scalars().all():
        await new_session.delete(obj)
    await new_session.commit()
    return {"status": "OK"}
