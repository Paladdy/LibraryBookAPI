from datetime import datetime
from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
import uuid # Уникальный идентификатор товара для поиска

class Book(SQLModel, table=True):
    __tablename__ = "books"

    #table=True означает, что класс должен стать
    #таблицей в базе данныхx

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4()

        )
    )

    title: str
    author: str
    description: str
    published_date: str
    price: int
    language: str

    created_at: datetime = Field(Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(Column(pg.TIMESTAMP, default=datetime.now))


    def __repr__(self):
        return f"<BOOK {self.title}>"

