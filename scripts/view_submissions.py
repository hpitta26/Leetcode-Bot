#!/usr/bin/env python3
"""View all submissions in the database"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database.db_manager import DatabaseManager
from src.utils.logger import setup_logger

def main():
    logger = setup_logger()
    
    db = DatabaseManager()
    submissions = db.get_all_submissions()
    
    if not submissions:
        logger.info("No submissions in database yet")
        db.close()
        return
    
    logger.info("All Submissions:")
    logger.blank()
    
    current_user = None
    for sub in submissions:
        if sub['username'] != current_user:
            if current_user is not None:
                logger.blank()
            current_user = sub['username']
            logger.info(f"{current_user}:")
        
        status = "✓" if sub['solved'] else "✗"
        logger.blank(f"  {status} {sub['problem_title']} ({sub['points']} points)")
    
    logger.blank()
    db.close()

if __name__ == "__main__":
    main()

