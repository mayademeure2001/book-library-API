from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from .base import TimeStampMixin

class WatchListBase(BaseModel):
    name: str
    description: Optional[str] = None
    movie_ids: List[int] = []

    @field_validator("name")
    def validate_name(cls, v: str):
        if len(v.strip()) < 1:
            raise ValueError("Name cannot be empty")
        return v.strip()

    @field_validator("movie_ids")
    def validate_movie_ids(cls, v: List[int]):
        if len(v) > 1000:
            raise ValueError("Too many movies in watch list (max 1000)")
        if len(v) != len(set(v)):
            raise ValueError("Duplicate movies in watch list")
        return v

class WatchListCreate(WatchListBase):
    pass

class WatchList(WatchListBase, TimeStampMixin):
    id: int
    
    class Config:
        from_attributes = True 