# app/models/user_follow.py
import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class UserFollow(Base):
    follower_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    followed_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # リレーションシップ
    follower = relationship("User", foreign_keys=[follower_id], back_populates="following")
    followed = relationship("User", foreign_keys=[followed_id], back_populates="followers")
