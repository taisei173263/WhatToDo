# app/models/task_like.py
import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class TaskLike(Base):
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("task.id"))
    user_id = Column(Integer, ForeignKey("user.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # リレーションシップ
    task = relationship("Task", back_populates="likes")
    user = relationship("User", back_populates="likes")
