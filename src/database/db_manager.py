"""Database manager for SQLite operations"""

import sqlite3
from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime

from .models import Competition, User, Problem, Submission


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
        self.cursor.execute(Competition.SCHEMA)
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
    
    def save_submission(self, username: str, problem_slug: str, solved: bool, competition_id: int, solved_at: str = None):
        """
        Save or update a submission record
        
        Args:
            username: LeetCode username
            problem_slug: Problem slug
            solved: Whether problem was solved
            competition_id: Competition ID
            solved_at: Timestamp when solved (ISO format string or None)
        """
        # Ensure user exists
        self.cursor.execute('''
            INSERT OR IGNORE INTO users (username, total_score, problems_solved)
            VALUES (?, 0, 0)
        ''', (username,))
        
        # Save submission
        self.cursor.execute('''
            INSERT OR REPLACE INTO submissions (username, problem_slug, competition_id, solved, solved_at, updated_at)
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ''', (username, problem_slug, competition_id, solved, solved_at))
        
        self.conn.commit()
    
    def get_leaderboard_data(self, competition_id: int = None) -> List[Dict[str, Any]]:
        """
        Get leaderboard data with scores
        
        Args:
            competition_id: Competition ID (uses current competition if None)
            
        Returns:
            List of users with their scores and solved problems, sorted by score descending
        """
        if competition_id is None:
            comp = self.get_current_competition()
            if not comp:
                return []
            competition_id = comp['id']
        
        query = '''
            SELECT 
                u.username,
                COALESCE(SUM(CASE WHEN s.solved THEN p.points ELSE 0 END), 0) as total_score,
                COUNT(CASE WHEN s.solved THEN 1 END) as problems_solved,
                u.last_updated
            FROM users u
            LEFT JOIN submissions s ON u.username = s.username AND s.competition_id = ?
            LEFT JOIN problems p ON s.problem_slug = p.slug
            GROUP BY u.username
            ORDER BY total_score DESC, problems_solved DESC, u.username ASC
        '''
        
        self.cursor.execute(query, (competition_id,))
        rows = self.cursor.fetchall()
        
        return [dict(row) for row in rows]
    
    def get_user_submissions(self, username: str, competition_id: int = None) -> List[Dict[str, Any]]:
        """
        Get all submissions for a specific user
        
        Args:
            username: LeetCode username
            competition_id: Competition ID (uses current competition if None)
            
        Returns:
            List of user's submissions with problem details
        """
        if competition_id is None:
            comp = self.get_current_competition()
            if not comp:
                return []
            competition_id = comp['id']
        
        query = '''
            SELECT 
                s.username,
                s.problem_slug,
                s.competition_id,
                p.title as problem_title,
                p.difficulty,
                p.points,
                s.solved,
                s.solved_at,
                s.updated_at
            FROM submissions s
            JOIN problems p ON s.problem_slug = p.slug
            WHERE s.username = ? AND s.competition_id = ?
            ORDER BY s.updated_at DESC
        '''
        
        self.cursor.execute(query, (username, competition_id))
        rows = self.cursor.fetchall()
        
        return [dict(row) for row in rows]
    
    def get_all_submissions(self, competition_id: int = None, all_competitions: bool = False) -> List[Dict[str, Any]]:
        """
        Get all submissions across all users
        
        Args:
            competition_id: Competition ID (uses current competition if None and all_competitions=False)
            all_competitions: If True, get submissions from all competitions
            
        Returns:
            List of all submissions with problem details
        """
        query = '''
            SELECT 
                s.username,
                s.problem_slug,
                s.competition_id,
                c.name as competition_name,
                p.title as problem_title,
                p.difficulty,
                p.points,
                s.solved,
                s.solved_at,
                s.updated_at
            FROM submissions s
            JOIN problems p ON s.problem_slug = p.slug
            JOIN competitions c ON s.competition_id = c.id
        '''
        
        params = []
        if not all_competitions:
            if competition_id is None:
                comp = self.get_current_competition()
                if not comp:
                    return []
                competition_id = comp['id']
            query += ' WHERE s.competition_id = ?'
            params.append(competition_id)
        
        query += ' ORDER BY s.competition_id, s.username, s.updated_at DESC'
        
        self.cursor.execute(query, params)
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
    
    def create_competition(self, name: str, start_date: str, end_date: str) -> int:
        """Create a new competition"""

        self.cursor.execute('''
            INSERT INTO competitions (name, start_date, end_date, has_run)
            VALUES (?, ?, ?, 0)
        ''', (name, start_date, end_date))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_current_competition(self) -> Optional[Dict[str, Any]]:
        """Get the most recent competition"""

        self.cursor.execute('''
            SELECT id, name, start_date, end_date, has_run, created_at
            FROM competitions
            ORDER BY created_at DESC
            LIMIT 1
        ''')
        row = self.cursor.fetchone()
        return dict(row) if row else None
    
    def mark_competition_run(self, competition_id: int):
        """Mark competition as run"""

        self.cursor.execute('''
            UPDATE competitions
            SET has_run = 1
            WHERE id = ?
        ''', (competition_id,))
        self.conn.commit()
    
    def revert_competition_run(self, competition_id: int):
        """Mark competition as not run (allows re-running)"""
        
        self.cursor.execute('''
            UPDATE competitions
            SET has_run = 0
            WHERE id = ?
        ''', (competition_id,))
        self.conn.commit()
    
    def close(self):
        """Close database connection"""
        self.conn.close()

