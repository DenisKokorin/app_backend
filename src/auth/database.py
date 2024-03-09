from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy import  Integer, String, Boolean, ARRAY, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from models.tables import role
from src.database import Base, get_async_session


class User(SQLAlchemyBaseUserTable[int], Base):
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    name: Mapped[str] = mapped_column(
        String(length=30), unique=True, nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )
    role_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(role.c.id)
    )
    library: Mapped[ARRAY(Integer)] = mapped_column(
        ARRAY(Integer)
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )



async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)