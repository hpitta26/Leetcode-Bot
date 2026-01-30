#!/usr/bin/env python3
"""
LeetCode Competition Bot - Main Entry Point

Run this script via cron to update the leaderboard.
Example crontab entry:
    0 8 * * * cd /path/to/leetcode-bot && python main.py
"""

import asyncio
from pathlib import Path


async def main():
    """Main execution function"""
    
    # 1. Load configuration
    print("Loading configuration...")
    
    # 2. Initialize database
    print("Initializing database...")
    
    # 3. Start scraper
    print("Starting scraper...")
    
    # 4. Scrape all users
    print("Scraping LeetCode data...")
    
    # 5. Save to database
    print("Saving to database...")
    
    print("✓ Done!")


if __name__ == "__main__":
    asyncio.run(main())

