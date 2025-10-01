from fastapi import APIRouter
from schemas.schemas import UserSchema
from models.models import UserModel
from repositories.settings import SessionDep
from bcrypt import hashpw, gensalt

router = APIRouter(prefix="/user", tags=['user'])

@router.post("")
async def create(user: UserSchema, new_session: SessionDep):
    hashed_pass = hashpw(user.password.encode(), gensalt(rounds=12)).decode()

    new_user = UserModel(
        name = user.name,
        login = user.login,
        password = hashed_pass
    )

    new_session.add(new_user)
    await new_session.commit()

    return {"status": "OK"}

