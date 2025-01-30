from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models import Book, User, UserBook
from app.schemas.bookcreate import BookCreate
from app.schemas.userbookcreate import UserBookCreate


async def create_book(db: AsyncSession, book_data: BookCreate) -> Book:
    db_book = Book(name=book_data.name, writer=book_data.writer)
    db.add(db_book)
    await db.commit()
    await db.refresh(db_book)
    return db_book


async def get_all_books(db: AsyncSession):
    result = await db.execute(select(Book))
    return result.scalars().all()


async def add_or_update_user_book_status(
    db: AsyncSession, username: str, userbook_data: UserBookCreate
):
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()

    if not user:
        return None, "User not found"

    book = await db.get(Book, userbook_data.book_id)
    if not book:
        return None, "Book not found"

    result = await db.execute(
        select(UserBook).where(
            (UserBook.user_id == user.id) & (UserBook.book_id == userbook_data.book_id)
        )
    )
    user_book = result.scalars().first()

    if user_book:
        user_book.status = userbook_data.status
    else:
        user_book = UserBook(user_id=user.id, book_id=book.id, status=userbook_data.status.value)
        db.add(user_book)

    await db.commit()
    await db.refresh(user_book)

    return user_book, None
