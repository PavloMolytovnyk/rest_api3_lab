from fastapi import FastAPI
from contextlib import asynccontextmanager
from api.books import router as books_router
from database import engine, Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="Library Cursor API", lifespan=lifespan)

app.include_router(books_router)

@app.get("/")
async def root():
    return {
        "message": "API is online",
        "pagination_type": "cursor_based",
        "docs_url": "/docs"
    }