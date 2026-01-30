#!/usr/bin/env python3
"""Show database information and statistics"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database.db_manager import DatabaseManager
from src.utils.logger import setup_logger

def main():
    logger = setup_logger()
    
    db = DatabaseManager()
    
    # Count problems
    db.cursor.execute("SELECT COUNT(*) FROM problems")
    problem_count = db.cursor.fetchone()[0]
    
    # Count users
    db.cursor.execute("SELECT COUNT(*) FROM users")
    user_count = db.cursor.fetchone()[0]
    
    # Count submissions
    db.cursor.execute("SELECT COUNT(*) FROM submissions")
    submission_count = db.cursor.fetchone()[0]
    
    # Count solved submissions
    db.cursor.execute("SELECT COUNT(*) FROM submissions WHERE solved = 1")
    solved_count = db.cursor.fetchone()[0]
    
    logger.info("Database Statistics:")
    logger.blank()
    logger.blank(f"  Problems: {problem_count}")
    logger.blank(f"  Users: {user_count}")
    logger.blank(f"  Total Submissions: {submission_count}")
    logger.blank(f"  Solved Submissions: {solved_count}")
    logger.blank()
    
    db.close()

if __name__ == "__main__":
    main()

