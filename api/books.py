from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import Optional
from database import get_db
from schemas.book import BookCreate, BookResponse, BookPaginationResponse
from services import book_service

router = APIRouter(prefix="/books", tags=["books"])

@router.get("/", response_model=BookPaginationResponse)
async def get_books(
    limit: int = Query(10, ge=1, le=100),
    cursor: Optional[UUID] = Query(None, description="ID останньої книги попередньої сторінки"),
    status: Optional[str] = None,
    author: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    books = await book_service.get_books(db, limit + 1, cursor, status, author)
    
    has_more = len(books) > limit
    items = books[:limit]
    
    next_cursor = items[-1].id if items and has_more else None

    return {
        "items": items,
        "next_cursor": next_cursor,
        "has_more": has_more
    }

@router.get("/{book_id}", response_model=BookResponse)
async def get_book(book_id: UUID, db: AsyncSession = Depends(get_db)):
    book = await book_service.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/", response_model=BookResponse, status_code=201)
async def create_book(book: BookCreate, db: AsyncSession = Depends(get_db)):
    return await book_service.create_book(db, book)

@router.delete("/{book_id}", status_code=204)
async def delete_book(book_id: UUID, db: AsyncSession = Depends(get_db)):
    await book_service.delete_book(db, book_id)
    return