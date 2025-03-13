# app/schemas/user.py
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


# ユーザー基本スキーマ
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    is_active: bool = True


# ユーザー作成リクエスト - 基底クラスから継承せずに独立して定義
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    is_active: bool = True


# ユーザー更新リクエスト
class UserUpdate(UserBase):
    password: Optional[str] = None


# データベースのユーザー (レスポンス用)
class UserInDBBase(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # orm_modeはv2では非推奨


# APIレスポンス用ユーザー
class User(UserInDBBase):
    pass
