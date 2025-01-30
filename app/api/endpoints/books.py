from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.bookcreate import BookCreate
from app.schemas.token import TokenData
from app.api.deps import get_current_user
from app.crud.book import create_book, get_all_books, add_or_update_user_book_status
from app.db.session import get_db
from app.schemas.bookresponse import BookResponse
from app.schemas.userbookcreate import UserBookCreate


router = APIRouter()


@router.post("/add_book", response_model=dict)
async def add_book(book: BookCreate, user: TokenData = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    db_book = await create_book(db, book)
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add book"
        )
    return {"message": f"Book has been successfully added by {user}"}


@router.get("/get_all_books", response_model=list[BookResponse])
async def get_books(db: AsyncSession = Depends(get_db)):
    return await get_all_books(db)


@router.post("/books/status/", response_model=dict)
async def add_book_status(
    userbook_data: UserBookCreate,
    db: AsyncSession = Depends(get_db),
    current_user: TokenData = Depends(get_current_user),
):
    user_book, error = await add_or_update_user_book_status(db, current_user.username, userbook_data)

    if error:
        raise HTTPException(status_code=404, detail=error)

    return {"message" : "Book status successfully added"}
