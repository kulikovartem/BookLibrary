from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Book
from app.schemas.bookcreate import BookCreate


async def create_book(db: AsyncSession, book_data: BookCreate) -> Book:
    db_book = Book(name=book_data.name, writer=book_data.writer)
    db.add(db_book)
    await db.commit()
    await db.refresh(db_book)
    return db_book
