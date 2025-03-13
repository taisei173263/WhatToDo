import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # リレーションシップの部分を更新

    # リレーションシップ
    tasks = relationship("Task", back_populates="owner")
    followers = relationship("UserFollow", foreign_keys="UserFollow.followed_id", back_populates="followed")
    following = relationship("UserFollow", foreign_keys="UserFollow.follower_id", back_populates="follower")
    likes = relationship("TaskLike", back_populates="user")
