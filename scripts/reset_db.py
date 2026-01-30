#!/usr/bin/env python3
"""Reset the database - clears all submissions but keeps problems"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database.db_manager import DatabaseManager
from src.utils.logger import setup_logger

def main():
    logger = setup_logger()
    
    logger.start("Resetting database...")
    
    db = DatabaseManager()
    
    # Clear submissions
    db.cursor.execute("DELETE FROM submissions")
    logger.success("Cleared all submissions")
    
    # Reset user stats
    db.cursor.execute("UPDATE users SET total_score = 0, problems_solved = 0")
    logger.success("Reset user statistics")
    
    db.conn.commit()
    db.close()
    
    logger.complete("Database reset complete!")

if __name__ == "__main__":
    main()

