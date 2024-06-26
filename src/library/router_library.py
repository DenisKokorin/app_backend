from typing import List

from fastapi import APIRouter, Depends
from fastapi_users import FastAPIUsers
from sqlalchemy import select

from models.tables import user, data_book
from src.auth.UserManager import get_user_manager
from src.auth.auth import auth_backend
from src.auth.database import User
from src.database import AsyncSession, get_async_session

router = APIRouter(
    prefix="/library",
    tags=["library"]
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user(active=True)

@router.get("/{user_id}", response_model=List[list])
async def get_user_library(user_id: int, session: AsyncSession = Depends(get_async_session), user_c: User = Depends(current_user)):
    if user_c.is_active:
        query = select(user.c.library).where(user.c.id == user_id)
        result = session.execute(query)
        return await result
    else:
        return {"not authorized"}

@router.get("/read/{book_id}")
async def read_book(book_id: int, session: AsyncSession = Depends(get_async_session), user_c: User = Depends(current_user)):
    if user_c.is_active:
        check = await session.execute(select(user.c.library).filter(user.c.id == user_c.id))
        library = check.scalars().first()
        if book_id in library:
            path = await session.execute(select(data_book).where(data_book.c.book_id == book_id))
            with open(path, "r") as file:
                book = file.read()
            return {"book": book}
        else:
            return {"you don't have this book"}
    else:
        return {"not authorized"}
