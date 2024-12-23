from pydantic import BaseModel

class Book(BaseModel):
    id: int
    title: str
    author: str
    description: str
    published_date: str
    price: int
    language: str

class BookUpdateModel(BaseModel):
    title: str
    author: str
    description: str
    language: str