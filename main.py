from fastapi import FastAPI
from app.api.endpoints import users
from app.db.session import init_db
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(users.router, prefix="/users", tags=["Users"])


@app.on_event("startup")
async def startup_event():
    await init_db()
