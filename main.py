"""
Run this script via cron to update the leaderboard.
Example crontab entry:
    0 8 * * * cd /path/to/leetcode-bot && python main.py
"""

import asyncio
from pathlib import Path
from src.utils.config_loader import load_config
from src.utils.logger import setup_logger
from src.database.db_manager import DatabaseManager
from src.scraper.leetcode_scraper import LeetCodeScraper


async def main():
    """Main execution function"""
    
    # Setup logger
    logger = setup_logger()
    db = None
    scraper = None
    
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
        scraper = LeetCodeScraper(
            headless=config['scraping']['headless'],
            timeout=config['scraping']['timeout']
        )
        await scraper.start()
        logger.success("Scraper started")
        
        # 4. Scrape all users
        logger.start(f"Scraping LeetCode data for {len(config['usernames'])} users...")
        problem_slugs = [p['slug'] for p in config['problems']]
        
        # First, get all recently solved problems for each user
        logger.blank()
        for username in config['usernames']:
            try:
                recently_solved = await scraper.get_user_recently_solved_problems(username)
                logger.info(f"{username}:")
                if recently_solved:
                    for problem in recently_solved[:20]:
                        # Check if it's a competition problem
                        if problem in problem_slugs:
                            logger.blank(f"  ✓ {problem} (competition)")
                        else:
                            logger.blank(f"    {problem}")
                    if len(recently_solved) > 20:
                        logger.blank(f"    ... and {len(recently_solved) - 20} more")
                else:
                    logger.blank("    No recent submissions found")
                logger.blank()
            except Exception as e:
                logger.warning(f"{username}: {str(e)}")
                logger.blank()
        
        # Now scrape with competition problems filter
        results = await scraper.scrape_all_users(config['usernames'], problem_slugs)
        logger.success(f"Data scraped for {len(results)} users")
        
        # 5. Save to database
        logger.start("Saving to database...")
        for user_result in results:
            username = user_result['username']
            if 'error' in user_result:
                logger.warning(f"Error for {username}: {user_result['error']}")
                continue
            
            for problem_slug, submission_data in user_result['submissions'].items():
                db.save_submission(
                    username=username,
                    problem_slug=problem_slug,
                    solved=submission_data['solved'],
                    solved_at=None  # TODO: Get actual solve time if available
                )
            
            db.update_user_stats(username)
        
        logger.success("Data saved successfully")
        
        # 6. Display leaderboard summary
        leaderboard = db.get_leaderboard_data()
        logger.complete(f"Bot completed! {len(leaderboard)} users tracked")
        
        # Display leaderboard
        if leaderboard:
            logger.blank()
            logger.info("Leaderboard:")
            for i, user in enumerate(leaderboard, 1):
                logger.blank(f"  {i}. {user['username']}: {user['total_score']} points ({user['problems_solved']} solved)")
            logger.blank()
        
    except Exception as e:
        logger.error_msg(f"Bot failed: {str(e)}")
        raise
    
    finally:
        if scraper:
            await scraper.close()
        if db:
            db.close()


if __name__ == "__main__":
    asyncio.run(main())

