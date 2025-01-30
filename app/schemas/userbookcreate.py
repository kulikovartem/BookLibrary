from pydantic import BaseModel
from app.schemas.status import Status


class UserBookCreate(BaseModel):
    book_id: int
    status: Status
