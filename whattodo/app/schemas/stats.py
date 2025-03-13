# app/schemas/stats.py
from datetime import date
from typing import Any, Dict, List, Optional  # noqa:F401

from pydantic import BaseModel


# 日次統計
class DailyStats(BaseModel):
    date: date
    total_tasks: int
    completed_tasks: int
    completion_rate: float  # パーセンテージ（0-100）


# 週次・月次統計
class PeriodStats(BaseModel):
    period: str  # "2023-W01" (週次) or "2023-01" (月次)
    total_tasks: int
    completed_tasks: int
    completion_rate: float  # パーセンテージ（0-100）


# ストリーク情報
class StreakInfo(BaseModel):
    current_streak: int
    longest_streak: int
    last_completed_date: Optional[date] = None


# 全体統計
class OverallStats(BaseModel):
    total_tasks: int
    completed_tasks: int
    completion_rate: float
    streak_info: StreakInfo
    daily_stats: List[DailyStats]
    weekly_stats: List[PeriodStats]
    monthly_stats: List[PeriodStats]
