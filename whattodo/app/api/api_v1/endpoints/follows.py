# app/api/api_v1/endpoints/follows.py
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User
from app.models.user_follow import UserFollow
from app.schemas.user import User as UserSchema

router = APIRouter()


@router.post("/{user_id}/follow", response_model=dict)
def follow_user(
    user_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Follow a user.
    """
    if user_id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail="You cannot follow yourself",
        )

    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    # Check if already following
    follow = (
        db.query(UserFollow)
        .filter(UserFollow.follower_id == current_user.id, UserFollow.followed_id == user_id)
        .first()
    )

    if follow:
        raise HTTPException(
            status_code=400,
            detail="Already following this user",
        )

    # Create follow relationship
    follow = UserFollow(follower_id=current_user.id, followed_id=user_id)
    db.add(follow)
    db.commit()

    return {"message": f"Now following user {user_id}"}


@router.delete("/{user_id}/follow", response_model=dict)
def unfollow_user(
    user_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Unfollow a user.
    """
    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    # Check if following
    follow = (
        db.query(UserFollow)
        .filter(UserFollow.follower_id == current_user.id, UserFollow.followed_id == user_id)
        .first()
    )

    if not follow:
        raise HTTPException(
            status_code=400,
            detail="Not following this user",
        )

    # Remove follow relationship
    db.delete(follow)
    db.commit()

    return {"message": f"Unfollowed user {user_id}"}


@router.get("/followers", response_model=List[UserSchema])
def get_followers(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get all followers of the current user.
    """
    follows = db.query(UserFollow).filter(UserFollow.followed_id == current_user.id).all()
    follower_ids = [follow.follower_id for follow in follows]
    followers = db.query(User).filter(User.id.in_(follower_ids)).all()

    return followers


@router.get("/following", response_model=List[UserSchema])
def get_following(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get all users that the current user is following.
    """
    follows = db.query(UserFollow).filter(UserFollow.follower_id == current_user.id).all()
    following_ids = [follow.followed_id for follow in follows]
    following = db.query(User).filter(User.id.in_(following_ids)).all()

    return following
