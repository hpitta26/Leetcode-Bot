"""Show database information and statistics"""

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
    
    # Count problems
    db.cursor.execute("SELECT COUNT(*) FROM problems")
    problem_count = db.cursor.fetchone()[0]
    
    # Count users
    db.cursor.execute("SELECT COUNT(*) FROM users")
    user_count = db.cursor.fetchone()[0]
    
    # Count competitions
    db.cursor.execute("SELECT COUNT(*) FROM competitions")
    comp_count = db.cursor.fetchone()[0]
    
    if comp:
        # Count submissions for current competition
        db.cursor.execute("SELECT COUNT(*) FROM submissions WHERE competition_id = ?", (comp['id'],))
        submission_count = db.cursor.fetchone()[0]
        
        # Count solved submissions for current competition
        db.cursor.execute("SELECT COUNT(*) FROM submissions WHERE solved = 1 AND competition_id = ?", (comp['id'],))
        solved_count = db.cursor.fetchone()[0]
        
        logger.info("Database Statistics:")
        logger.blank()
        logger.blank(f"  Current Competition: {comp['name']}")
        logger.blank(f"  Total Competitions: {comp_count}")
        logger.blank(f"  Problems: {problem_count}")
        logger.blank(f"  Users: {user_count}")
        logger.blank()
        logger.blank(f"  Current Comp Submissions: {submission_count}")
        logger.blank(f"  Current Comp Solved: {solved_count}")
        logger.blank()
    else:
        logger.info("Database Statistics:")
        logger.blank()
        logger.blank(f"  Competitions: {comp_count}")
        logger.blank(f"  Problems: {problem_count}")
        logger.blank(f"  Users: {user_count}")
        logger.blank()
    
    db.close()

if __name__ == "__main__":
    main()

