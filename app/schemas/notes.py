from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
import uuid

class NoteCreate(BaseModel):
    title: str = Field(
        min_length=3,
        max_length=50
    )
    content: str | None = None
    is_pinned: bool = False
    
class NoteUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=3,
        max_length=50
    )
    content: str | None = None
    is_pinned: bool | None = None
    
class NoteResponse(BaseModel):
    id: int
    title: str
    content: str | None
    is_pinned: bool
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )