# app/api/api_v1/api.py
from fastapi import APIRouter

from app.api.api_v1.endpoints import (
    follows,
    likes,
    login,
    stats,
    tasks,
    timeline,
    users,
)

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(follows.router, prefix="/users", tags=["follows"])
api_router.include_router(likes.router, prefix="/tasks", tags=["likes"])
api_router.include_router(timeline.router, prefix="/timeline", tags=["timeline"])
api_router.include_router(stats.router, prefix="/stats", tags=["stats"])
