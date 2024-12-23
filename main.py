from fastapi.exceptions import HTTPException
from fastapi import FastAPI, Header, status
from typing import Optional, List
from src.books.book_data import books
from src.books.schemas import Book, BookUpdateModel





app = FastAPI()



