#!/usr/bin/env python3
"""View the current leaderboard"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database.db_manager import DatabaseManager
from src.utils.logger import setup_logger

def main():
    logger = setup_logger()
    
    db = DatabaseManager()
    leaderboard = db.get_leaderboard_data()
    
    if not leaderboard:
        logger.info("No users in leaderboard yet")
        db.close()
        return
    
    logger.info("Current Leaderboard:")
    logger.blank()
    
    for i, user in enumerate(leaderboard, 1):
        logger.blank(f"  {i}. {user['username']}: {user['total_score']} points ({user['problems_solved']} solved)")
    
    logger.blank()
    db.close()

if __name__ == "__main__":
    main()

