#-----------------А
from sqlmodel.ext.asyncio.session import AsyncSession
#-----------------
from .schemas import BookCreateModel, BookUpdateModel
from sqlmodel import select, desc
from .models import Book
from datetime import datetime

class BookService:
    # ---------------------------GET ALL

    async def get_all_books(self, session:AsyncSession): # выполняются любые виды CR
        statement = select(Book).order_by(desc(Book.created_at)) # SELECT * FROM BOOKS ORDER BY CREATED_AT
        result = await session.exec(statement)

        return result.all()

    #---------------------------GET ONE

    async def get_a_book(self, book_uid: str, session:AsyncSession):
        statement = select(Book).where(Book.uid == book_uid)
        result = await session.exec(statement)
        book = result.first() # возвращает первую запись при совпадении uid

        return book if book is not None else None
    # ---------------------------CREATE ONE

    async def create_a_book(self, book_data:BookCreateModel, session:AsyncSession):
        book_data_dict = book_data.model_dump()

        new_book = Book(**book_data_dict) # Наподобе __init__ создаем параметры для экземпляра new_book


        new_book.published_date = datetime.strptime(book_data_dict["published_date"], "%Y-%m-%d")

        session.add(new_book) # Добавляем объект в тип данных session.

        await session.commit() # INSERT INTO

        return new_book # Возвращаем книгу на полку, после того, как создали, чтобы могли использовать в других модулях

    # ---------------------------UPDATE ONE

    async def update_a_book(self, book_uid:str, update_data:BookUpdateModel, session:AsyncSession):
        book_to_update = await self.get_a_book(book_uid, session)
        update_data_dict = update_data.model_dump()

        if book_to_update is not None:
            for key, value in update_data_dict.items():
                setattr(book_to_update, key, value)

            await session.commit()

            return book_to_update
        else:
            return None

    # ---------------------------DELETE ONE

    async def delete_a_book(self, book_uid:str, session:AsyncSession):
        book_to_delete = self.get_a_book(book_uid, session)

        if book_to_delete is not None:
            await session.delete(book_to_delete)

            await session.commit()

            return {}

        else:
            return None


