from typing import List

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from bcrypt import hashpw, gensalt

from schemas.schemas import UserCreate, UserPasswordChange, UserPublic, UserUpdate
from models.models import UserModel
from repositories.settings import SessionDep

router = APIRouter(prefix="/user", tags=['user'])

def _hash_password(raw: str) -> str:
    return hashpw(raw.encode(), gensalt(rounds=12)).decode()

def _to_public(u: UserModel) -> UserPublic:
    return UserPublic(
        id=u.id,
        email=u.email,
        login=u.login,
        createdAt=u.createdAt,
        updatedAt=u.updatedAt
    )

@router.post("", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def create(payload: UserCreate, session: SessionDep):

    user = UserModel(
        email=payload.email,
        login=payload.login,
        password=_hash_password(payload.password)
    )

    session.add(user)

    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=409, detail="login or email already exists")
    await session.refresh(user)
    return _to_public(user)

@router.get("", response_model=List[UserPublic])
async def list_users(session: SessionDep):
    stmt = select(UserModel).order_by(UserModel.id.asc())
    users = await session.execute(stmt).scalars().all()
    return [ _to_public(user) for user in users ]

@router.get("/{user_id}", response_model=UserPublic)
async def get_user(user_id: int, session: SessionDep):
    stmt = select(UserModel).where(UserModel.id == user_id)
    user = await session.execute(stmt).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return _to_public(user)

@router.patch("/{user_id}", response_model=UserPublic)
async def update_user(user_id:int, payload: UserUpdate, session: SessionDep):
    stmt = select(UserModel).where(UserModel.id == user_id)
    user = await session.execute(stmt).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    if payload.login is not None:
        user.login = payload.login
    if payload.email is not None:
        user.email = payload.email
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=409, detail="login or email already exists")
    await session.refresh(user)
    return _to_public(user)

@router.patch("/{user_id}", response_model=UserPublic)
async def change_password(user_id: int, payload: UserPasswordChange, session: SessionDep):
    stmt = select(UserModel).where(UserModel.id == user_id)
    user = await session.execute(stmt).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    user.password = _hash_password(payload.new_password)
    await session.commit()
    return _to_public(user)

@router.delete("/{user_id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, session: SessionDep):
    stmt = select(UserModel).where(UserModel.id == user_id)
    res = await session.execute(stmt)
    await session.commit()
    return