"""View all submissions in the database"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database.db_manager import DatabaseManager
from src.utils.logger import setup_logger

def main():
    logger = setup_logger()
    
    db = DatabaseManager()
    submissions = db.get_all_submissions(all_competitions=True)
    
    if not submissions:
        logger.info("No submissions in database yet")
        db.close()
        return
    
    logger.info("All Submissions (All Competitions):")
    logger.blank()
    
    current_comp = None
    current_user = None
    for sub in submissions:
        # Show competition header
        if sub['competition_id'] != current_comp:
            if current_comp is not None:
                logger.blank()
            current_comp = sub['competition_id']
            logger.info(f"Competition: {sub['competition_name']}")
            current_user = None  # Reset user when competition changes
        
        # Show user header
        if sub['username'] != current_user:
            current_user = sub['username']
            logger.blank(f"  {current_user}:")
        
        status = "✓" if sub['solved'] else "✗"
        logger.blank(f"    {status} {sub['problem_title']} ({sub['points']} points)")
    
    logger.blank()
    db.close()

if __name__ == "__main__":
    main()

