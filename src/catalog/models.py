from pydantic import BaseModel
from sqlalchemy import LargeBinary


class Book(BaseModel):
    id: int
    title: str
    author: str
    year: int
    description: str
    genre: str
    number_of_pages: int
    access: int
    publishing_house: str

class Review(BaseModel):
    book_id: int
    user_id: int
    rating: int
    text: str