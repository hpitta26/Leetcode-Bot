"""Data models for the competition"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    """Represents a competition participant"""
    username: str
    total_score: int = 0
    problems_solved: int = 0
    last_updated: Optional[datetime] = None


@dataclass
class Problem:
    """Represents a LeetCode problem"""
    slug: str
    title: str
    difficulty: str
    points: int


@dataclass
class Submission:
    """Represents a user's submission for a problem"""
    username: str
    problem_slug: str
    solved: bool
    solved_at: Optional[datetime] = None

