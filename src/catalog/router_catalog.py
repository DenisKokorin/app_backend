from typing import List
from fastapi import Depends, APIRouter
from fastapi_users import FastAPIUsers
from sqlalchemy import select, insert, update, delete
from models.tables import book, user, review, data_book
from src.auth.UserManager import get_user_manager
from src.auth.auth import auth_backend
from src.auth.database import User
from src.catalog.models import Book, Review
from src.database import get_async_session, AsyncSession
from src.library.models import BookData


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



@router.post("/")
async def add_book(new_book: Book, data: BookData, session: AsyncSession = Depends(get_async_session), user: User = Depends(current_user)):
    if user.is_superuser:
        stmt1 = insert(book).values(**new_book.dict())
        stmt2 = insert(data_book).values(**data.dict())
        await session.execute(stmt1)
        await session.execute(stmt2)
        await session.commit()
        return {"status": "200"}
    else:
        return {"not superuser"}

@router.patch("/")
async def update_book(book_id: int, updated_book: Book, data: BookData, session: AsyncSession = Depends(get_async_session), user: User = Depends(current_user)):
    if user.is_superuser:
        stmt1 = update(book).where(book.c.id == book_id).values(**updated_book.dict())
        stmt2 = update(data_book).where(data_book.c.book_id == book_id).values(**data.dict())
        await session.execute(stmt1)
        await session.execute(stmt2)
        await session.commit()
        return {"status": "200"}
    else:
        return {"not superuser"}

@router.delete("/")
async def delete_book(book_id: int, session: AsyncSession = Depends(get_async_session), user: User = Depends(current_user)):
    if user.is_superuser:
        stmt1 = delete(book).where(book.c.id == book_id)
        stmt2 = delete(data_book).where(data_book.c.book_id == book_id)
        await session.execute(stmt1)
        await session.execute(stmt2)
        await session.commit()
        return {"status": "200"}
    else:
        return {"not superuser"}


@router.get("/{book_id}", response_model=List[list])
async def get_book_id(book_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(book).where(book.c.id == book_id)
    result = session.execute(query)
    return await result


@router.post("/{book_id}")
async def add_book_to_library(book_id: int, session: AsyncSession = Depends(get_async_session), user_c: User = Depends(current_user)):
    if user_c.is_active:
        query_check_book = await session.execute(select(user.c.library).filter(user.c.id == user_c.id))
        l = query_check_book.scalars().first()
        if not book_id in l:
            query_check_access = select(book.c.access).where(book.c.id == book_id)
            result_check_access = (await session.execute(query_check_access)).scalars().all()
            if user_c.role_id == result_check_access[0]:
                query_get_library = await session.execute(select(user.c.library).filter(user.c.id == user_c.id))
                library = query_get_library.scalars().first()
                library.append(book_id)
                query_update_library = update(user).where(user.c.id == user_c.id).values(library = library)
                await session.execute(query_update_library)
                await session.commit()
                return library
            else:
                return {"no access to the book"}
        else:
            return {"the book has already been added"}
    else:
        return {"not authorized"}

@router.delete("/{book_id}")
async def delete_from_library(book_id: int, session: AsyncSession = Depends(get_async_session), user_c: User = Depends(current_user)):
    if user_c.is_active:
        query_get_library = await session.execute(select(user.c.library).filter(user.c.id == user_c.id))
        library = query_get_library.scalars().first()
        if book_id in library:
            library.remove(book_id)
            query_update_library = update(user).where(user.c.id == user_c.id).values(library = library)
            await session.execute(query_update_library)
            await session.commit()
            return library
        else:
            return {"there is no book in the library"}
    else:
        return {"not authorized"}


@router.get("/{book_id}/reviews", response_model= List[list])
async def get_reviews(book_id: int, session: AsyncSession = Depends(get_async_session)):
    check = select(review).where(review.c.book_id == book_id)
    r = await session.execute(check)
    if r.first():
        query = select(review).filter(review.c.book_id == book_id)
        result = await session.execute(query)
        return result
    else:
        return {"this book has no reviews"}

@router.post("/{book_id}/reviews")
async def write_review(new_review: Review, bookid: int, session: AsyncSession = Depends(get_async_session), user_c: User = Depends(current_user)):
    if user_c.is_active:
        check = select(review).where(user.c.id == user_c.id, review.c.book_id == bookid)
        result = await session.execute(check)
        if not result.first():
            query = insert(review).values(book_id = bookid, user_id = user_c.id, rating = new_review.rating, text = new_review.text)
            await session.execute(query)
            await session.commit()
            return {"status": "200"}
        else:
            return {"you have already added a review"}
    else:
        return {"not authorized"}

@router.patch("/{book_id}/reviews")
async def change_review(new_review: Review, bookid: int, session: AsyncSession = Depends(get_async_session), user_c: User = Depends(current_user)):
    if user_c.is_active:
        check = select(review).where(user.c.id == user_c.id, review.c.book_id == bookid)
        result = await session.execute(check)
        if result.first():
            query = update(review).where(book.c.id == bookid, user.c.id == user_c.id).values(book_id = bookid, user_id = user_c.id, rating = new_review.rating, text = new_review.text)
            await session.execute(query)
            await session.commit()
            return {"status":"200"}
        return {"you didn't add a review"}
    else:
        return {"not authorized"}
    
@router.delete("/{book_id}/reviews")
async def delete_review(bookid: int, session: AsyncSession = Depends(get_async_session), user_c: User = Depends(current_user)):
    if user_c.is_active:
        check = select(review).where(user.c.id == user_c.id, review.c.book_id == bookid)
        result = await session.execute(check)
        if result.first():
            query = delete(review).where(book.c.id == bookid, user.c.id == user_c.id)
            await session.execute(query)
            await session.commit()
            return {"status":"200"}
        return {"you didn't add a review"}
    else:
        return {"not authorized"}
