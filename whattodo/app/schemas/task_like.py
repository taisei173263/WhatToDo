# app/schemas/task_like.py
from datetime import datetime
from typing import Optional  # noqa: F401

from pydantic import BaseModel


# いいね基本スキーマ
class TaskLikeBase(BaseModel):
    task_id: int
    user_id: int


# いいね作成リクエスト
class TaskLikeCreate(TaskLikeBase):
    pass


# データベースのいいね (レスポンス用)
class TaskLikeInDBBase(TaskLikeBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# APIレスポンス用いいね
class TaskLike(TaskLikeInDBBase):
    pass
