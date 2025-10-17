from sqlalchemy.schema import PrimaryKeyConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, func, BigInteger, Text, SmallInteger, DateTime
from typing import List, Optional
from datetime import datetime

class Base(DeclarativeBase):
    pass


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(index=True)
    login: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column(Text)
    createdat: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updatedat: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    thoughts: Mapped[List["ThoughtModel"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    moods: Mapped[List["MoodModel"]] = relationship(back_populates="user", cascade="all, delete-orphan")

class ThoughtModel(Base):
    __tablename__ = "thoughts"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    createdat: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)


    stages: Mapped[list["StageModel"]] = relationship(back_populates="thought", cascade="all, delete-orphan")
    user: Mapped[UserModel] = relationship(back_populates="thoughts")


class StageModel(Base):
    __tablename__ = "stages"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    thought_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("thoughts.id", ondelete="CASCADE"), index=True)
    stage: Mapped[int] = mapped_column(SmallInteger)
    capture: Mapped[str] = mapped_column(Text)
    createdat: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)

    thought:Mapped[ThoughtModel] = relationship(back_populates="stages")

class MoodModel(Base):
    __tablename__ = "moods"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), index=True)

    mood: Mapped[str] = mapped_column(Text)
    createdat: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False,
                                                index=True)

    user: Mapped[UserModel] = relationship(back_populates="moods")