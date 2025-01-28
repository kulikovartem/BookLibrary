from fastapi import FastAPI
from app.api.endpoints import users, books
from app.db.session import init_db
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(books.router, prefix="/books", tags=["Books"])


@app.on_event("startup")
async def startup_event():
    await init_db()
