from datetime import datetime, date
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from .base import TimeStampMixin

class BookBase(BaseModel):
    title: str
    description: Optional[str] = None
    isbn: str | int = Field(min_length=10, max_length=13)
    publication_date: date
    genre: str
    author_id: int
    total_pages: int

    @field_validator("publication_date")
    def validate_publication_date(cls, v: date):
        if v > date.today():
            raise ValueError("Publication date cannot be in the future")
        return v

    @field_validator("total_pages")
    def validate_total_pages(cls, v: int):
        if v < 1:
            raise ValueError("Total pages must be positive")
        if v > 5000:
            raise ValueError("Book seems too long, please verify total pages")
        return v

    @field_validator("isbn")
    def validate_isbn(cls, v: str | int):
        cleaned_isbn = v.replace("-", "").replace(" ", "")
        if not cleaned_isbn.isdigit():
            raise ValueError("ISBN must contain only digits, hyphens, or spaces")
        if len(cleaned_isbn) not in [10, 13]:
            raise ValueError("ISBN must be 10 or 13 digits long")
        return v

    @field_validator("title")
    def validate_title(cls, v: str):
        if len(v.strip()) < 1:
            raise ValueError("Title cannot be empty")
        return v.strip()

    @field_validator("genre")
    def validate_genre(cls, v: str):
        if len(v.strip()) < 2:
            raise ValueError("Genre must be at least 2 characters long")
        return v.strip()

class BookCreate(BookBase):
    pass

class Book(BookBase, TimeStampMixin):
    id: int
    
    class Config:
        from_attributes = True 