from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.bookcreate import BookCreate
from app.api.deps import get_current_user
from app.crud.book import create_book
from app.db.session import get_db


router = APIRouter()


@router.post("/add_book", response_model=dict)
async def add_book(book: BookCreate, user: str = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    db_book = await create_book(db, book)
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add book"
        )
    return {"message": f"Book has been successfully added by {user}"}

