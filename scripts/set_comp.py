"""Set up a new competition from config"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database.db_manager import DatabaseManager
from src.utils.config_loader import load_config
from src.utils.logger import setup_logger

def main():
    logger = setup_logger()
    
    logger.start("Setting up new competition...")
    
    # Load config
    config = load_config()
    comp_config = config['competition']
    
    db = DatabaseManager()
    
    # Check if there's already a competition
    current_comp = db.get_current_competition()
    if current_comp:
        logger.warning(f"Existing competition found: '{current_comp['name']}'")
        logger.blank()
        response = input("Create new competition anyway? (y/N): ")
        if response.lower() != 'y':
            logger.info("Cancelled")
            db.close()
            return
        logger.blank()
    
    # Create new competition
    comp_id = db.create_competition(
        name=comp_config['name'],
        start_date=comp_config['start_date'],
        end_date=comp_config['end_date']
    )
    
    # Initialize problems
    db.init_problems(config['problems'])
    
    logger.success(f"Competition '{comp_config['name']}' created (ID: {comp_id})")
    logger.blank()
    logger.info("Competition details:")
    logger.blank(f"  Name: {comp_config['name']}")
    logger.blank(f"  Start: {comp_config['start_date']}")
    logger.blank(f"  End: {comp_config['end_date']}")
    logger.blank(f"  Problems: {len(config['problems'])}")
    logger.blank(f"  Participants: {len(config['usernames'])}")
    logger.blank()
    
    db.close()
    
    logger.complete("Competition setup complete! Run 'make run' to start.")

if __name__ == "__main__":
    main()

