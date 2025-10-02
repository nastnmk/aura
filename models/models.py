from sqlalchemy.schema import PrimaryKeyConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, func
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
    password: Mapped[str]
    createdAt: Mapped[datetime] = mapped_column(default=func.now())
    updatedAt: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now(), nullable=False)

    thoughts: Mapped[List["ThoughtModel"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )


class ThoughtModel(Base):
    __tablename__ = "thoughts"

    id: Mapped[int]
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    stage: Mapped[int]
    capture: Mapped[str]
    date: Mapped[str]

    user: Mapped[UserModel] = relationship(back_populates="thoughts")

    __table_args__ = (
        PrimaryKeyConstraint("id", "stage", name="pk_thoughts_id_stage"),
    )
