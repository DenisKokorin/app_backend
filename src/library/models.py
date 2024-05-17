from pydantic import BaseModel

class BookData(BaseModel):
    book_id: int
    data: str
