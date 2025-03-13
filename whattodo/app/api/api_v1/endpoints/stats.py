# app/api/api_v1/endpoints/stats.py
import calendar
from datetime import date, datetime, timedelta
from typing import Any, Dict, List  # noqa:F401

from fastapi import APIRouter, Depends, HTTPException, Query  # noqa:F401
from sqlalchemy import and_, func, or_  # noqa:F401
from sqlalchemy.orm import Session

from app.api import deps
from app.models.task import Task
from app.models.user import User
from app.schemas.stats import DailyStats, OverallStats, PeriodStats, StreakInfo

router = APIRouter()


def get_date_range(days: int):
    """過去n日間の日付範囲を取得"""
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days - 1)
    return start_date, end_date


def get_streak_info(db: Session, user_id: int) -> StreakInfo:
    """ストリーク情報を計算"""
    # 完了したタスクの日付を取得（昇順）
    completed_dates = (
        db.query(func.date(Task.updated_at))
        .filter(Task.owner_id == user_id, Task.is_completed)  # Changed from Task.is_completed == True
        .distinct()
        .order_by(func.date(Task.updated_at))
        .all()
    )

    completed_dates = [d[0] for d in completed_dates]

    if not completed_dates:
        return StreakInfo(current_streak=0, longest_streak=0, last_completed_date=None)

    # 現在のストリークを計算
    current_streak = 0
    today = datetime.now().date()

    # 最後の完了日が今日または昨日の場合のみストリークが続いている
    last_date = completed_dates[-1]
    days_since_last = (today - last_date).days

    if days_since_last <= 1:  # 今日または昨日
        current_date = last_date
        current_streak = 1

        # 過去日をさかのぼってチェック
        for i in range(len(completed_dates) - 2, -1, -1):
            prev_date = completed_dates[i]
            days_diff = (current_date - prev_date).days

            if days_diff == 1:  # 連続した日
                current_streak += 1
                current_date = prev_date
            elif days_diff > 1:  # 連続していない
                break

    # 最長ストリークを計算
    longest_streak = 1
    current_run = 1

    for i in range(1, len(completed_dates)):
        days_diff = (completed_dates[i] - completed_dates[i - 1]).days

        if days_diff == 1:  # 連続した日
            current_run += 1
        else:  # 連続していない
            longest_streak = max(longest_streak, current_run)
            current_run = 1

    longest_streak = max(longest_streak, current_run)

    return StreakInfo(
        current_streak=current_streak, longest_streak=longest_streak, last_completed_date=completed_dates[-1]
    )


@router.get("/overview", response_model=OverallStats)
def get_overall_stats(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get overall statistics for the current user.
    """
    start_date, end_date = get_date_range(days)

    # 全体の統計
    total_tasks = db.query(func.count(Task.id)).filter(Task.owner_id == current_user.id).scalar()

    completed_tasks = (
        db.query(func.count(Task.id)).filter(Task.owner_id == current_user.id, Task.is_completed).scalar()  # Changed
    )

    completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

    # ストリーク情報
    streak_info = get_streak_info(db, current_user.id)

    # 日次統計
    daily_stats = []
    current_date = start_date

    while current_date <= end_date:
        day_tasks = (
            db.query(func.count(Task.id))
            .filter(
                Task.owner_id == current_user.id,
                func.date(Task.created_at) <= current_date,
                or_(Task.due_date.is_(None), func.date(Task.due_date) >= current_date),
            )
            .scalar()
        )

        day_completed = (
            db.query(func.count(Task.id))
            .filter(
                Task.owner_id == current_user.id,
                Task.is_completed,
                func.date(Task.updated_at) == current_date,  # Changed
            )
            .scalar()
        )

        day_rate = (day_completed / day_tasks * 100) if day_tasks > 0 else 0

        daily_stats.append(
            DailyStats(
                date=current_date, total_tasks=day_tasks, completed_tasks=day_completed, completion_rate=day_rate
            )
        )

        current_date += timedelta(days=1)

    # 週次統計
    weekly_stats = []
    current_week_start = start_date - timedelta(days=start_date.weekday())

    while current_week_start <= end_date:
        week_end = current_week_start + timedelta(days=6)

        week_tasks = (
            db.query(func.count(Task.id))
            .filter(
                Task.owner_id == current_user.id,
                func.date(Task.created_at) <= week_end,
                or_(Task.due_date.is_(None), func.date(Task.due_date) >= current_week_start),
            )
            .scalar()
        )

        week_completed = (
            db.query(func.count(Task.id))
            .filter(
                Task.owner_id == current_user.id,
                Task.is_completed,  # Changed
                func.date(Task.updated_at) >= current_week_start,
                func.date(Task.updated_at) <= week_end,
            )
            .scalar()
        )

        week_rate = (week_completed / week_tasks * 100) if week_tasks > 0 else 0

        week_str = f"{current_week_start.isocalendar()[0]}-W{current_week_start.isocalendar()[1]:02d}"

        weekly_stats.append(
            PeriodStats(
                period=week_str, total_tasks=week_tasks, completed_tasks=week_completed, completion_rate=week_rate
            )
        )

        current_week_start += timedelta(days=7)

    # 月次統計
    monthly_stats = []
    current_month_start = date(start_date.year, start_date.month, 1)

    while current_month_start <= end_date:
        month_days = calendar.monthrange(current_month_start.year, current_month_start.month)[1]
        month_end = date(current_month_start.year, current_month_start.month, month_days)

        month_tasks = (
            db.query(func.count(Task.id))
            .filter(
                Task.owner_id == current_user.id,
                func.date(Task.created_at) <= month_end,
                or_(Task.due_date.is_(None), func.date(Task.due_date) >= current_month_start),
            )
            .scalar()
        )

        month_completed = (
            db.query(func.count(Task.id))
            .filter(
                Task.owner_id == current_user.id,
                Task.is_completed,  # Changed
                func.date(Task.updated_at) >= current_month_start,
                func.date(Task.updated_at) <= month_end,
            )
            .scalar()
        )

        month_rate = (month_completed / month_tasks * 100) if month_tasks > 0 else 0

        month_str = f"{current_month_start.year}-{current_month_start.month:02d}"

        monthly_stats.append(
            PeriodStats(
                period=month_str, total_tasks=month_tasks, completed_tasks=month_completed, completion_rate=month_rate
            )
        )

        # 次の月へ
        if current_month_start.month == 12:
            current_month_start = date(current_month_start.year + 1, 1, 1)
        else:
            current_month_start = date(current_month_start.year, current_month_start.month + 1, 1)

    return OverallStats(
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        completion_rate=completion_rate,
        streak_info=streak_info,
        daily_stats=daily_stats,
        weekly_stats=weekly_stats,
        monthly_stats=monthly_stats,
    )


@router.get("/streak", response_model=StreakInfo)
def get_user_streak(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get the current user's task completion streak.
    """
    return get_streak_info(db, current_user.id)
