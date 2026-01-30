"""Data models for the competition"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, ClassVar, List


@dataclass
class Competition:
    """Represents a competition"""
    name: str
    start_date: str
    end_date: str
    has_run: bool = False
    created_at: Optional[datetime] = None
    
    SCHEMA: ClassVar[str] = '''
        CREATE TABLE IF NOT EXISTS competitions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            has_run BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    '''


@dataclass
class User:
    """Represents a competition participant"""
    username: str
    total_score: int = 0
    problems_solved: int = 0
    last_updated: Optional[datetime] = None
    
    SCHEMA: ClassVar[str] = '''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            total_score INTEGER DEFAULT 0,
            problems_solved INTEGER DEFAULT 0,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    '''


@dataclass
class Problem:
    """Represents a LeetCode problem"""
    slug: str
    title: str
    difficulty: str
    points: int
    
    SCHEMA: ClassVar[str] = '''
        CREATE TABLE IF NOT EXISTS problems (
            slug TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            points INTEGER NOT NULL
        )
    '''


@dataclass
class Submission:
    """Represents a user's submission for a problem"""
    username: str
    problem_slug: str
    solved: bool
    competition_id: int
    solved_at: Optional[datetime] = None
    
    SCHEMA: ClassVar[str] = '''
        CREATE TABLE IF NOT EXISTS submissions (
            username TEXT NOT NULL,
            problem_slug TEXT NOT NULL,
            competition_id INTEGER NOT NULL,
            solved BOOLEAN NOT NULL,
            solved_at TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (username, problem_slug, competition_id),
            FOREIGN KEY (problem_slug) REFERENCES problems(slug),
            FOREIGN KEY (username) REFERENCES users(username),
            FOREIGN KEY (competition_id) REFERENCES competitions(id)
        )
    '''

