from pydantic import BaseModel
import uuid
from datetime import datetime
# Модели данных, которые возвращаются или принимаются от пользователя

class Book(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    description: str
    published_date: str
    price: int
    language: str
    created_at: datetime
    updated_at: datetime

class BookCreateModel(BaseModel):
    title: str
    author: str
    description: str
    price: int
    language: str

class BookUpdateModel(BaseModel):
    title: str
    author: str
    description: str
    price: int
    language: str