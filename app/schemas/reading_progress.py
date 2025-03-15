from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from enum import Enum
from .base import TimeStampMixin

class ReadingStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"
    DROPPED = "dropped"

class ReadingProgressBase(BaseModel):
    book_id: int
    status: ReadingStatus
    current_page: int | str | None = None
    total_pages: Optional[int] = None
    notes: Optional[str] = None

    @field_validator("current_page")
    def validate_current_page(cls, v: int | str | None, values):
        if v is None:
            return v
        if isinstance(v, int) and v < 0:
            raise ValueError("Current page cannot be negative")
        return v

    @field_validator("notes")
    def validate_notes(cls, v: Optional[str]):
        if v is not None and len(v) > 500:
            raise ValueError("Notes must not exceed 500 characters")
        return v

class ReadingProgressCreate(ReadingProgressBase):
    pass

class ReadingProgress(ReadingProgressBase, TimeStampMixin):
    id: int
    
    class Config:
        from_attributes = True 