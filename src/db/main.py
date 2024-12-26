from sqlmodel import text, SQLModel
from src.config import Config
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine


# Создаем движок на основе config.py
engine = create_async_engine(
    url=Config.DATABASE_URL,
    echo=True # Логгирование запросов SQL (для отладки)
)

# ----------------- Тут мы только создаем саму таблицу -----------
# Создаем функцию для дальнейших транзакций в БД
async def db_init(): # Инициализируем подключение к БД
    async with engine.begin() as connection: # with позволяет открыть из закрыть соединение.
                                             # async гарантирует commit или rollback

        from src.books.models import Book

        await connection.run_sync(SQLModel.metadata.create_all) # Создаем все таблицы из models.py


#---------Создаем саму сессию для БД чтобы можно было выполнять к ней запросы
async def get_session() -> AsyncSession:

    Session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False # после комита данные в сессии останутся
    )

    # Пока играем с игрушкой, когда наиграемся - кладем, но потом снова можем играть
    async with Session() as session:
        yield session # Передается только тем функциям, которые ее запрашивают. механизм с yield - инжекция зависимостей.
                      # Вне вызова через другие функции не работает




