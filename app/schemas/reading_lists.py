from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from .base import TimeStampMixin

class ReadingListBase(BaseModel):
    name: str
    description: Optional[str] = None
    book_ids: List[int] = []

    @field_validator("name")
    def validate_name(cls, v: str):
        if len(v.strip()) < 1:
            raise ValueError("Name cannot be empty")
        return v.strip()

    @field_validator("book_ids")
    def validate_book_ids(cls, v: List[int]):
        if len(v) > 1000:
            raise ValueError("Too many books in reading list (max 1000)")
        if len(v) != len(set(v)):
            raise ValueError("Duplicate books in reading list")
        return v

class ReadingListCreate(ReadingListBase):
    pass

class ReadingList(ReadingListBase, TimeStampMixin):
    id: int
    
    class Config:
        from_attributes = True 