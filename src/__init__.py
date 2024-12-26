from fastapi import FastAPI
from src.books.routes import books_router
from contextlib import asynccontextmanager
from src.db.main import db_init

# Отслеживаем подключение к бд
@asynccontextmanager
async def life_span(app: FastAPI):
    print(f"Сервер работает. Запускаем писю в космос :)...")
    await db_init()
    yield
    print(f"Сервер остановился. Печалька :(")

version = "v1"
app = FastAPI(
    title="LibraryBookAPI",
    description="A REST API for a book review web service",
    version=version,
    lifespan=life_span,
)

#Префикс нужен для того, чтобы избежать дублирования и сгруппировать наши
#эндпоинты для книг
app.include_router(books_router, prefix=f"/api/{version}/books", tags= ["books"])