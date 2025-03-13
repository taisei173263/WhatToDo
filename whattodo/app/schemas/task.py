# app/schemas/task.py
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# タスク基本スキーマ
class TaskBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: bool = False
    due_date: Optional[datetime] = None
    privacy_level: str = "followers"  # public, followers, private


# タスク作成リクエスト - 基底クラスから継承せずに独立して定義
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    is_completed: bool = False
    due_date: Optional[datetime] = None
    privacy_level: str = "followers"


# タスク更新リクエスト
class TaskUpdate(TaskBase):
    pass


# データベースのタスク (レスポンス用)
class TaskInDBBase(TaskBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # orm_mode は Pydantic v2 では from_attributes に変更


# APIレスポンス用タスク
class Task(TaskInDBBase):
    pass
