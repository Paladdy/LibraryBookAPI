from sqlmodel import create_engine, text, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
from src.config import Config

# Создаем движок на основе config.py
engine = AsyncEngine(
    create_engine(
    url=Config.DATABASE_URL,
    echo=True # Логгирование запросов SQL (для отладки)
))

# Создаем функцию для дальнейших транзакций в БД
async def db_init():
    async with engine.begin() as connection:
        from src.books.models import Book

        await connection.run_sync(SQLModel.metadata.create_all)





