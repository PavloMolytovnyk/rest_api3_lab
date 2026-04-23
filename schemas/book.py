from pydantic import BaseModel, Field
from uuid import UUID
from typing import List, Optional
import enum

class BookStatus(str, enum.Enum):
    available = "available"
    borrowed = "borrowed"

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

class BookPaginationResponse(BaseModel):
    items: List[BookResponse]
    next_cursor: Optional[UUID] = None
    has_more: bool