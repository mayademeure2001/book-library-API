from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from enum import Enum
from .base import TimeStampMixin

class ViewingStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"
    DROPPED = "dropped"

class ViewingHistoryBase(BaseModel):
    movie_id: int
    status: ViewingStatus
    current_minute: int | str | None = None
    runtime_minutes: Optional[int] = None
    notes: Optional[str] = None

    @field_validator("current_minute")
    def validate_current_minute(cls, v: int | str | None, values):
        if v is None:
            return v
        if isinstance(v, int) and v < 0:
            raise ValueError("Current minute cannot be negative")
        return v

    @field_validator("notes")
    def validate_notes(cls, v: Optional[str]):
        if v is not None and len(v) > 500:
            raise ValueError("Notes must not exceed 500 characters")
        return v

class ViewingHistoryCreate(ViewingHistoryBase):
    pass

class ViewingHistory(ViewingHistoryBase, TimeStampMixin):
    id: int
    
    class Config:
        from_attributes = True 