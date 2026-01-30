"""Show current competition status"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database.db_manager import DatabaseManager
from src.utils.logger import setup_logger

def main():
    logger = setup_logger()
    
    db = DatabaseManager()
    
    # Get current competition
    comp = db.get_current_competition()
    
    if not comp:
        logger.warning("No competition found")
        logger.info("Run 'make set-comp' to create a competition first")
        db.close()
        return
    
    # Get problem count
    db.cursor.execute("SELECT COUNT(*) FROM problems")
    problem_count = db.cursor.fetchone()[0]
    
    # Get user count
    db.cursor.execute("SELECT COUNT(*) FROM users")
    user_count = db.cursor.fetchone()[0]
    
    logger.info("Current Competition:")
    logger.blank()
    logger.blank(f"  Name: {comp['name']}")
    logger.blank(f"  Period: {comp['start_date']} to {comp['end_date']}")
    logger.blank(f"  Status: {'✓ Completed' if comp['has_run'] else '○ Not run yet'}")
    logger.blank(f"  Created: {comp['created_at']}")
    logger.blank()
    logger.blank(f"  Problems: {problem_count}")
    logger.blank(f"  Users: {user_count}")
    logger.blank()
    
    if comp['has_run']:
        logger.info("Competition has been run. Use 'make revert-run' to allow re-running.")
    else:
        logger.info("Competition ready. Run 'make run' to start.")
    
    db.close()

if __name__ == "__main__":
    main()

