from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from uuid import UUID
from datetime import datetime

class ProfileUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    avatar_initials: Optional[str] = Field(None, max_length=3)

class ProfileResponse(BaseModel):
    id: UUID
    email: str
    full_name: str
    role: str
    avatar_initials: Optional[str]
    created_at: datetime
    total_metrics_logged: Optional[int] = 0

    class Config:
        from_attributes = True