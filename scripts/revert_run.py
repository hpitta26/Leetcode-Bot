"""Revert competition run status to allow re-running"""

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
    
    if not comp['has_run']:
        logger.info(f"Competition '{comp['name']}' has not been run yet")
        db.close()
        return
    
    logger.warning(f"Competition '{comp['name']}' has been run")
    logger.blank()
    logger.info("This will:")
    logger.blank("  1. Clear all submissions from this run")
    logger.blank("  2. Reset user statistics")
    logger.blank("  3. Mark competition as not run")
    logger.blank()
    logger.warning("This will delete submission data!")
    logger.blank()
    
    response = input("Revert run and clear data? (y/N): ")
    if response.lower() != 'y':
        logger.info("Cancelled")
        db.close()
        return
    
    logger.blank()
    logger.start("Reverting run status...")
    
    # Clear submissions for THIS competition only
    db.cursor.execute("DELETE FROM submissions WHERE competition_id = ?", (comp['id'],))
    count = db.cursor.rowcount
    logger.success(f"Cleared {count} submissions for this competition")
    
    # Reset user stats (will be recalculated if other competitions exist)
    db.cursor.execute("UPDATE users SET total_score = 0, problems_solved = 0")
    logger.success("Reset user statistics")
    
    # Mark as not run
    db.revert_competition_run(comp['id'])
    logger.success("Marked as not run")
    
    db.conn.commit()
    
    logger.blank()
    logger.complete("Competition reverted! You can now run 'make run' again")
    
    db.close()

if __name__ == "__main__":
    main()

