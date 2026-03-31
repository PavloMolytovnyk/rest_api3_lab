from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, asc
from models.book_model import Book
from uuid import UUID

async def get_all(db: AsyncSession, limit: int, cursor: UUID = None, status=None, author=None):
    # Сортуємо за ID, щоб курсор працював коректно
    query = select(Book).order_by(asc(Book.id)).limit(limit)
    
    if cursor:
        query = query.where(Book.id > cursor)
        
    if status:
        query = query.filter(Book.status == status)
    if author:
        query = query.filter(Book.author == author)
    
    result = await db.execute(query)
    return result.scalars().all()

async def get_by_id(db: AsyncSession, book_id: UUID):
    result = await db.execute(select(Book).filter(Book.id == book_id))
    return result.scalar_one_or_none()

async def add(db: AsyncSession, book_data: dict):
    new_book = Book(**book_data)
    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)
    return new_book

async def delete_book(db: AsyncSession, book_id: UUID):
    await db.execute(delete(Book).where(Book.id == book_id))
    await db.commit()