"""Database manager for SQLite operations"""

import sqlite3
from typing import List, Dict, Any
from pathlib import Path
from datetime import datetime

from .models import User, Problem, Submission


class DatabaseManager:
    """Manages SQLite database operations"""
    
    def __init__(self, db_path: str = "db.sqlite"):
        """
        Initialize database manager
        
        Args:
            db_path: Path to SQLite database file (default: db.sqlite)
        """
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.init_database()
    
    def init_database(self):
        """Create database tables if they don't exist using model schemas"""
        
        # Create tables in order (respect foreign key dependencies)
        self.cursor.execute(User.SCHEMA)
        self.cursor.execute(Problem.SCHEMA)
        self.cursor.execute(Submission.SCHEMA)
        
        self.conn.commit()
    
    def init_problems(self, problems: List[Dict[str, Any]]):
        """
        Initialize problems from configuration
        
        Args:
            problems: List of problem dictionaries with slug, title, difficulty, points
        """
        for problem in problems:
            self.cursor.execute('''
                INSERT OR REPLACE INTO problems (slug, title, difficulty, points)
                VALUES (?, ?, ?, ?)
            ''', (problem['slug'], problem['title'], problem['difficulty'], problem['points']))
        
        self.conn.commit()
    
    def save_submission(self, username: str, problem_slug: str, solved: bool, solved_at: str = None):
        """
        Save or update a submission record
        
        Args:
            username: LeetCode username
            problem_slug: Problem slug
            solved: Whether problem was solved
            solved_at: Timestamp when solved (ISO format string or None)
        """
        # Ensure user exists
        self.cursor.execute('''
            INSERT OR IGNORE INTO users (username, total_score, problems_solved)
            VALUES (?, 0, 0)
        ''', (username,))
        
        # Save submission
        self.cursor.execute('''
            INSERT OR REPLACE INTO submissions (username, problem_slug, solved, solved_at, updated_at)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        ''', (username, problem_slug, solved, solved_at))
        
        self.conn.commit()
    
    def get_leaderboard_data(self) -> List[Dict[str, Any]]:
        """
        Get leaderboard data with scores
        
        Returns:
            List of users with their scores and solved problems, sorted by score descending
        """
        query = '''
            SELECT 
                u.username,
                COALESCE(SUM(CASE WHEN s.solved THEN p.points ELSE 0 END), 0) as total_score,
                COUNT(CASE WHEN s.solved THEN 1 END) as problems_solved,
                u.last_updated
            FROM users u
            LEFT JOIN submissions s ON u.username = s.username
            LEFT JOIN problems p ON s.problem_slug = p.slug
            GROUP BY u.username
            ORDER BY total_score DESC, problems_solved DESC, u.username ASC
        '''
        
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        
        return [dict(row) for row in rows]
    
    def get_user_submissions(self, username: str) -> List[Dict[str, Any]]:
        """
        Get all submissions for a specific user
        
        Args:
            username: LeetCode username
            
        Returns:
            List of user's submissions with problem details
        """
        query = '''
            SELECT 
                s.username,
                s.problem_slug,
                p.title as problem_title,
                p.difficulty,
                p.points,
                s.solved,
                s.solved_at,
                s.updated_at
            FROM submissions s
            JOIN problems p ON s.problem_slug = p.slug
            WHERE s.username = ?
            ORDER BY s.updated_at DESC
        '''
        
        self.cursor.execute(query, (username,))
        rows = self.cursor.fetchall()
        
        return [dict(row) for row in rows]
    
    def get_all_submissions(self) -> List[Dict[str, Any]]:
        """
        Get all submissions across all users
        
        Returns:
            List of all submissions with problem details
        """
        query = '''
            SELECT 
                s.username,
                s.problem_slug,
                p.title as problem_title,
                p.difficulty,
                p.points,
                s.solved,
                s.solved_at,
                s.updated_at
            FROM submissions s
            JOIN problems p ON s.problem_slug = p.slug
            ORDER BY s.username, s.updated_at DESC
        '''
        
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        
        return [dict(row) for row in rows]
    
    def update_user_stats(self, username: str):
        """
        Update cached user statistics
        
        Args:
            username: LeetCode username
        """
        query = '''
            UPDATE users
            SET 
                total_score = (
                    SELECT COALESCE(SUM(p.points), 0)
                    FROM submissions s
                    JOIN problems p ON s.problem_slug = p.slug
                    WHERE s.username = ? AND s.solved = 1
                ),
                problems_solved = (
                    SELECT COUNT(*)
                    FROM submissions s
                    WHERE s.username = ? AND s.solved = 1
                ),
                last_updated = CURRENT_TIMESTAMP
            WHERE username = ?
        '''
        
        self.cursor.execute(query, (username, username, username))
        self.conn.commit()
    
    def close(self):
        """Close database connection"""
        self.conn.close()

