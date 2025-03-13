# app/api/api_v1/endpoints/likes.py
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.models.task import Task
from app.models.task_like import TaskLike
from app.models.user import User
from app.schemas.task_like import TaskLike as TaskLikeSchema  # noqa: F401

router = APIRouter()


@router.post("/{task_id}/like", response_model=dict)
def like_task(
    task_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Like a task.
    """
    # Check if task exists
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    # Check if already liked
    like = db.query(TaskLike).filter(TaskLike.task_id == task_id, TaskLike.user_id == current_user.id).first()

    if like:
        raise HTTPException(
            status_code=400,
            detail="Already liked this task",
        )

    # Create like
    like = TaskLike(task_id=task_id, user_id=current_user.id)
    db.add(like)
    db.commit()

    return {"message": f"Liked task {task_id}"}


@router.delete("/{task_id}/like", response_model=dict)
def unlike_task(
    task_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Unlike a task.
    """
    # Check if task exists
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    # Check if liked
    like = db.query(TaskLike).filter(TaskLike.task_id == task_id, TaskLike.user_id == current_user.id).first()

    if not like:
        raise HTTPException(
            status_code=400,
            detail="Task not liked",
        )

    # Remove like
    db.delete(like)
    db.commit()

    return {"message": f"Unliked task {task_id}"}


@router.get("/{task_id}/likes", response_model=int)
def get_task_likes_count(
    task_id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get task likes count.
    """
    # Check if task exists
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    # Count likes
    likes_count = db.query(TaskLike).filter(TaskLike.task_id == task_id).count()

    return likes_count


@router.get("/{task_id}/likes/users", response_model=List[int])
def get_task_likes_users(
    task_id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get users who liked a task.
    """
    # Check if task exists
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    # Get user IDs who liked the task
    likes = db.query(TaskLike).filter(TaskLike.task_id == task_id).all()
    user_ids = [like.user_id for like in likes]

    return user_ids
