#!/usr/bin/env python3
"""
LeetCode Competition Bot - Main Entry Point

Run this script via cron to update the leaderboard.
Example crontab entry:
    0 8 * * * cd /path/to/leetcode-bot && python main.py
"""

import asyncio
from pathlib import Path
from src.utils.config_loader import load_config
from src.utils.logger import setup_logger
from src.database.db_manager import DatabaseManager


async def main():
    """Main execution function"""
    
    # Setup logger
    logger = setup_logger()
    
    try:
        logger.start("Starting LeetCode Competition Bot")
        
        # 1. Load configuration
        logger.start("Loading configuration...")
        config = load_config()
        logger.success("Configuration loaded")
        
        # 2. Initialize database
        logger.start("Initializing database...")
        db = DatabaseManager()
        db.init_problems(config['problems'])
        logger.success(f"Database initialized with {len(config['problems'])} problems")
        
        # 3. Start scraper
        logger.start("Starting scraper...")
        # TODO: Initialize scraper
        logger.success("Scraper started")
        
        # 4. Scrape all users
        logger.start("Scraping LeetCode data...")
        # TODO: Scrape data for each user in config['usernames']
        logger.success(f"Data scraped for {len(config['usernames'])} users")
        
        # 5. Save to database
        logger.start("Saving to database...")
        # TODO: Save scraped data
        logger.success("Data saved successfully")
        
        # 6. Display leaderboard summary
        leaderboard = db.get_leaderboard_data()
        logger.complete(f"Bot completed! {len(leaderboard)} users tracked")
        
        # Close database connection
        db.close()
        
    except Exception as e:
        logger.error_msg(f"Bot failed: {str(e)}")
        raise


if __name__ == "__main__":
    asyncio.run(main())

