
from pydantic import BaseModel

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
    rating: float



