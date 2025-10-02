from fastapi import  APIRouter
from schemas.schemas import ThoughtSchema, ThoughtUpdSchema
from models.models import ThoughtModel
from repositories.settings import SessionDep, session
from sqlalchemy import select

router = APIRouter(prefix="/thoughts", tags=['thoughts'])

@router.get("")
async def get(new_session:SessionDep):
    query = select(ThoughtModel)
    result = await new_session.execute(query)
    return result.scalars().all()

@router.post("")
async def create(thought: ThoughtSchema, new_session: SessionDep):
    new_thought = ThoughtModel(
        id = thought.id,
        user_id = thought.user_id,
        stage = thought.stage,
        capture = thought.capture,
        date = "now"
    )

    new_session.add(new_thought)
    await new_session.commit()

    return {"status": "OK"}

@router.delete("")
async def delete(thought_id: int, new_session: SessionDep):
    query = select(ThoughtModel).where(ThoughtModel.id == thought_id)    # искать с условием
    result = await new_session.execute(query)
    result = result.scalars().all()
    for i in result:
        await new_session.delete(i)

    await new_session.commit()
    return {"status": "OK"}

@router.patch("")
async def edit(thought_detail: ThoughtUpdSchema, new_session: SessionDep):
    query = select(ThoughtModel).where(ThoughtModel.id == thought_detail.id, ThoughtModel.stage == thought_detail.stage)
    result = await new_session.execute(query)
    result = result.scalar_one_or_none()

    updates = thought_detail.model_dump(exclude_unset=True)     # тут мы просто в найденный экземпляр вставляем новые значения
    for field, value in updates.items():
        setattr(result, field, value)

    await new_session.commit()
    return {"status": "OK"}
