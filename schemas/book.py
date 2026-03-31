from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional
from models.book_model import BookStatus

class BookCreate(BaseModel):
    title: str = Field(min_length=1)
    author: str
    description: Optional[str] = None
    status: BookStatus
    year: int = Field(gt=0)

class BookResponse(BaseModel):
    id: UUID
    title: str
    author: str
    description: Optional[str]
    status: BookStatus
    year: int

    class Config:
        from_attributes = True