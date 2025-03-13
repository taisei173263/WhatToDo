# app/schemas/timeline.py
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas.user import User


# タイムラインアイテムスキーマ
class TimelineItem(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    is_completed: bool
    due_date: Optional[datetime] = None
    privacy_level: str
    created_at: datetime
    updated_at: datetime
    owner_id: int
    owner: User
    likes_count: int
    liked_by_me: bool

    class Config:
        from_attributes = True
