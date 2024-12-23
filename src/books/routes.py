from fastapi import APIRouter, status, HTTPException, Header
from typing import List
from src.books.book_data import books
from src.books.schemas import Book, BookUpdateModel

"""Используем отдельный роут для книг"""
books_router = APIRouter()


#----GET ALL
@books_router.get('/', response_model=List[Book])
async def get_all_books():
    return books

#----GET ONE
@books_router.get('/{book_id}')
async def get_book(book_id: int) -> dict:
    for book in books:
        if book['id'] == book_id:
            return book
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Book not found')

#----POST
@books_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_a_book(book_data: Book) -> dict:
    new_book = book_data.model_dump() #Конвертируем в dict

    books.append(new_book)

    return new_book

#----PATCH ONE
@books_router.patch("/{book_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_a_book(book_id: int, book_update_data:BookUpdateModel) -> dict:
    for book in books:
        if book['id'] == book_id:
            book['title'] = book_update_data.title
            book['author'] = book_update_data.author
            book['description'] = book_update_data.description
            book['language'] = book_update_data.language

            return book

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book not found')


#----DELETE ONE
@books_router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_a_book(book_id: int):
    for book in books:
        if book['id'] == book_id:
            books.remove(book)

            return {}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book not found')

#----Test MAIN
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
        user_agent:str = Header(None),
        host:str = Header(None),
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