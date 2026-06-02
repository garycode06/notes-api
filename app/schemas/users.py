from pydantic import BaseModel, ConfigDict, EmailStr, Field
from datetime import datetime
import uuid

class UserUpdate(BaseModel):
    username: str | None = Field(default=None, min_length=3, max_length=50)
    email: EmailStr | None = None

class PasswordUpdate(BaseModel):
    current_password: str = Field(min_length=1, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)

class UserResponse(BaseModel):
    id: uuid.UUID
    username: str
    email: EmailStr
    actif: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
