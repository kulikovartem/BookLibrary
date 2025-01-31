from pydantic import BaseModel


class BookResponse(BaseModel):
    id: int
    name: str
    writer: str

    class Config:
        orm_mode = True
