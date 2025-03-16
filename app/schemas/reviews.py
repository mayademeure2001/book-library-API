from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from .base import TimeStampMixin

class ReviewBase(BaseModel):
    rating: int | str = Field(description="Rating as number (1-5) or text")
    comment: Optional[str] = None
    movie_id: int

    @field_validator("rating")
    def validate_rating(cls, v: int | str):
        if isinstance(v, int) and not (1 <= v <= 5):
            raise ValueError("Rating must be between 1 and 5")
        return v

    @field_validator("comment")
    def validate_comment(cls, v: Optional[str]):
        if v is not None:
            if len(v.strip()) < 5:
                raise ValueError("Comment must be at least 5 characters long")
            if len(v) > 1000:
                raise ValueError("Comment must not exceed 1000 characters")
        return v

class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase, TimeStampMixin):
    id: int
    
    class Config:
        from_attributes = True 