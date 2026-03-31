import uuid
import enum
from sqlalchemy import Column, String, Integer, Enum as SQLEnum, Text
from sqlalchemy.dialects.postgresql import UUID
from database import Base

class BookStatus(str, enum.Enum):
    available = "available"
    borrowed = "borrowed"

class Book(Base):
    __tablename__ = "books"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(SQLEnum(BookStatus), default=BookStatus.available)
    year = Column(Integer, nullable=False)