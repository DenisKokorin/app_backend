from typing import List
from fastapi import Depends, APIRouter
from fastapi_users import FastAPIUsers
from sqlalchemy import select, insert, update, delete
from models.tables import book, user
from src.auth.UserManager import get_user_manager
from src.auth.auth import auth_backend
from src.auth.database import User
from src.catalog.models import Book
from src.database import get_async_session, AsyncSession



router = APIRouter (
    prefix="/catalog",
    tags=["catalog"]
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user(active=True)


@router.get("/",response_model=List[list])
async def get_books(session: AsyncSession = Depends(get_async_session)):
    query = select(book).limit(30)
    result = session.execute(query)
    return await result


@router.get("/{book_id}", response_model=List[list])
async def get_book_id(book_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(book).where(book.c.id == book_id)
    result = session.execute(query)
    return await result


@router.post("/")
async def add_book(new_book: Book, session: AsyncSession = Depends(get_async_session), user: User = Depends(current_user)):
    if user.is_superuser:
        stmt = insert(book).values(**new_book.dict())
        await session.execute(stmt)
        await session.commit()
        return {"status": "200"}
    else:
        return {"not superuser"}

@router.patch("/{book_id}")
async def update_book(book_id: int, updated_book: Book, session: AsyncSession = Depends(get_async_session), user: User = Depends(current_user)):
    if user.is_superuser:
        stmt = update(book).where(book.c.id == book_id).values(**updated_book.dict())
        await session.execute(stmt)
        await session.commit()
        return {"status": "200"}
    else:
        return {"not superuser"}

@router.delete("/{book_id}")
async def delete_book(book_id: int, session: AsyncSession = Depends(get_async_session), user: User = Depends(current_user)):
    if user.is_superuser:
        stmt = delete(book).where(book.c.id == book_id)
        await session.execute(stmt)
        await session.commit()
        return {"status": "200"}
    else:
        return {"not superuser"}

@router.post("/{book_id}/add-to-library")
async def add_book_to_library(book_id: int, session: AsyncSession = Depends(get_async_session), user_c: User = Depends(current_user)):
    if user_c.is_active:
        query_check_access = select(book.c.access).where(book.c.id == book_id)
        result_check_access = (await session.execute(query_check_access)).scalars().all()
        if user_c.role_id == result_check_access[0]:
            result = await session.execute(select(user.c.library).filter(user.c.id == user_c.id))
            library = result.scalars().first()
            library.append(book_id)
            query_update_library = update(user).where(user.c.id == user_c.id).values(library = library)
            await session.execute(query_update_library)
            await session.commit()
            return library
        else:
            return {"no access to the book"}
    else:
        return {"not authorized"}

