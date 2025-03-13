# app/api/api_v1/endpoints/timeline.py
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query  # noqa: F401
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.api import deps
from app.models.task import Task
from app.models.task_like import TaskLike
from app.models.user import User
from app.models.user_follow import UserFollow
from app.schemas.timeline import TimelineItem

router = APIRouter()


@router.get("/", response_model=List[TimelineItem])
def get_timeline(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get timeline of tasks from followed users.
    """
    # Get IDs of users that the current user follows
    follows = db.query(UserFollow.followed_id).filter(UserFollow.follower_id == current_user.id).all()
    following_ids = [follow[0] for follow in follows]

    # Include current user's ID to show their tasks in timeline too
    user_ids = following_ids + [current_user.id]

    # Get tasks from these users with privacy level that allows viewing
    tasks = (
        db.query(Task)
        .filter(
            Task.owner_id.in_(user_ids),
            # Only show public tasks or followers-only tasks (current user is a follower)
            Task.privacy_level.in_(["public", "followers"]),
        )
        .order_by(Task.created_at.desc())
        .offset(skip)
        .limit(limit)
        .options(joinedload(Task.owner))  # Eager load the owner relationship
        .all()
    )

    # For each task, add likes count and whether current user liked it
    timeline_items = []
    for task in tasks:
        # Count likes for this task
        likes_count = db.query(func.count(TaskLike.id)).filter(TaskLike.task_id == task.id).scalar()

        # Check if current user liked this task
        liked_by_me = (
            db.query(TaskLike).filter(TaskLike.task_id == task.id, TaskLike.user_id == current_user.id).first()
            is not None
        )

        # Create TimelineItem
        timeline_item = {**task.__dict__, "owner": task.owner, "likes_count": likes_count, "liked_by_me": liked_by_me}

        timeline_items.append(timeline_item)

    return timeline_items


@router.get("/explore", response_model=List[TimelineItem])
def explore_public_tasks(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Explore public tasks from all users.
    """
    # Get public tasks from all users
    tasks = (
        db.query(Task)
        .filter(Task.privacy_level == "public")
        .order_by(Task.created_at.desc())
        .offset(skip)
        .limit(limit)
        .options(joinedload(Task.owner))  # Eager load the owner relationship
        .all()
    )

    # For each task, add likes count and whether current user liked it
    timeline_items = []
    for task in tasks:
        # Count likes for this task
        likes_count = db.query(func.count(TaskLike.id)).filter(TaskLike.task_id == task.id).scalar()

        # Check if current user liked this task
        liked_by_me = (
            db.query(TaskLike).filter(TaskLike.task_id == task.id, TaskLike.user_id == current_user.id).first()
            is not None
        )

        # Create TimelineItem
        timeline_item = {**task.__dict__, "owner": task.owner, "likes_count": likes_count, "liked_by_me": liked_by_me}

        timeline_items.append(timeline_item)

    return timeline_items
