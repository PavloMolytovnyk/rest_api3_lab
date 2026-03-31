from fastapi import FastAPI
from api.books import router as books_router
from database import engine, Base

app = FastAPI(title="Library Cursor API")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(books_router)

@app.get("/")
async def root():
    return {"message": "API is online", "pagination": "cursor"}