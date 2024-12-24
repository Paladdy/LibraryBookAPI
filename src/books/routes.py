from fastapi import APIRouter, status, HTTPException, Header, Depends
from typing import List
from src.books.schemas import Book, BookUpdateModel, BookCreateModel
from src.db.main import get_session
from src.books.service import BookService
from sqlmodel.ext.asyncio.session import AsyncSession

"""Используем отдельный роут для книг"""
books_router = APIRouter()
book_service = BookService()

#-------------------- Создаем уже сами данные внутри таблиц

# ----GET ALL
@books_router.get('/', response_model=List[Book])
async def get_all_books(session: AsyncSession = Depends(get_session)): # Запрашиваем из service = yield session
    books = await book_service.get_all_books(session) # Вызываем сервис из service.py #В параметр session передается сессия БД
    return books

# Вообщем то используем инжектор для того, чтобы в каждом эндпойнте не создавать заново сессию для БД

# ----GET ONE
@books_router.get('/{book_uid}', response_model=Book)
async def get_a_book(book_uid: str, session: AsyncSession = Depends(get_session)) -> dict:
    book = await book_service.get_a_book(book_uid, session)
    if book:
        return book
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Book not found')


# ----POST
@books_router.post('/',
                   status_code=status.HTTP_201_CREATED,
                   response_model=Book)

async def create_a_book(book_data: BookCreateModel, session: AsyncSession = Depends(get_session)) -> dict:
    new_book = await book_service.create_a_book(book_data, session)  # Конвертируем в dict
    return new_book


# ----PATCH ONE
@books_router.patch("/{book_uid}", status_code=status.HTTP_202_ACCEPTED)
async def update_a_book(book_uid: str, book_update_data: BookUpdateModel,
                        session: AsyncSession = Depends(get_session)) -> dict:
    updated_book = await book_service.update_a_book(book_uid, book_update_data, session)

    if updated_book:
        return updated_book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book not found')




# ----DELETE ONE
@books_router.delete("/{book_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_a_book(book_uid: str, session: AsyncSession = Depends(get_session)):
    book_to_delete = await book_service.delete_a_book(book_uid, session)

    if book_to_delete:
        return None
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book not found')



# ----Test MAIN
@books_router.get("/")
async def read_root():  # асинхронная функция - корутина
    return {"message": "Сервер запущен"}


@books_router.post("/create_book", status_code=201)
async def create_book(book_data: Book):
    return {
        "title": book_data.title,
        "author": book_data.author,
        "description": book_data.description,
    }


@books_router.get("/get_headers", status_code=200)
async def get_headers(
        accept: str = Header(None),
        content_type: str = Header(None),
        user_agent: str = Header(None),
        host: str = Header(None),
):
    # Добавляем в словарь значения ключей пользователя
    request_headers = {}

    # Клиент: "Я приму любой формат данных" "Accept": "*/*",
    request_headers["Accept"] = accept

    # Сервер: "Тогда я решаю отправить тебе любой тип данных"
    request_headers["Content-Type"] = content_type

    # Отображает с какого браузера пришел запрос от клиента.
    # Нужно для адаптации под конкретный браузер
    request_headers["User-Agent"] = user_agent

    # Доменное имя или ip к чему клиент отправляет запрос
    request_headers["Host"] = host

    return request_headers
