from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from .base import TimeStampMixin

class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = None

    @field_validator("name")
    def validate_name(cls, v: str):
        if len(v.strip()) < 2:
            raise ValueError("Name must be at least 2 characters long")
        return v.strip()

    @field_validator("bio")
    def validate_bio(cls, v: Optional[str]):
        if v is not None:
            if len(v) > 5000:
                raise ValueError("Bio is too long (max 5000 characters)")
        return v

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase, TimeStampMixin):
    id: int
    
    class Config:
        from_attributes = True 