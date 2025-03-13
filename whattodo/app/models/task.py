import datetime
import enum

from sqlalchemy import (  # Enum,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class PrivacyLevel(enum.Enum):
    public = "public"
    followers = "followers"
    private = "private"


class Task(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text, nullable=True)
    is_completed = Column(Boolean, default=False)
    due_date = Column(DateTime, nullable=True)
    privacy_level = Column(String, default="followers")  # EnumTypeはSQLiteでは直接サポートされていないので単純化
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="tasks")
    # 以下は後で実装
    likes = relationship("TaskLike", back_populates="task")
