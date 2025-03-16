from datetime import datetime, date
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from .base import TimeStampMixin

class MovieBase(BaseModel):
    title: str
    description: Optional[str] = None
    imdb_id: str = Field(pattern=r'^tt\d{7,8}$')
    release_date: date
    genre: str
    director_id: int
    runtime_minutes: int

    @field_validator("release_date")
    def validate_release_date(cls, v: date):
        if v > date.today():
            raise ValueError("Release date cannot be in the future")
        return v

    @field_validator("runtime_minutes")
    def validate_runtime_minutes(cls, v: int):
        if v < 1:
            raise ValueError("Runtime must be positive")
        if v > 600:
            raise ValueError("Movie seems too long, please verify runtime")
        return v

    @field_validator("imdb_id")
    def validate_imdb_id(cls, v: str):
        cleaned_id = v.strip().lower()
        if not cleaned_id.startswith('tt'):
            raise ValueError("IMDB ID must start with 'tt'")
        if not cleaned_id[2:].isdigit():
            raise ValueError("IMDB ID must contain only digits after 'tt'")
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

class MovieCreate(MovieBase):
    pass

class Movie(MovieBase, TimeStampMixin):
    id: int
    
    class Config:
        from_attributes = True 