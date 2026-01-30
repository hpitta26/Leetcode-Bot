# LeetCode Competition Bot

A bot that tracks LeetCode problem submissions for competition participants and generates a leaderboard.

## Features

- Scrapes LeetCode user profiles using Playwright
- Tracks which problems each user has solved
- Designed to run via cron (daily updates)
- Stores data in SQLite database

## Setup

### 1. Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

### 2. Configure Competition

Edit `config.yaml`:
- Add participant usernames
- Add problems to track (with slugs and points)
- Set competition dates

### 4. Setup Cron (Optional)

Run daily at 8 AM:

```bash
# Edit crontab
crontab -e

# Add this line:
0 8 * * * cd /path/to/leetcode-bot && /path/to/venv/bin/python main.py >> logs/cron.log 2>&1
```

## Utility Scripts

Similar to npm scripts, you can use `make` commands to manage the bot:

```bash
make run          # Run the LeetCode bot
make leaderboard  # View current leaderboard
make submissions  # View all submissions
make info         # Show database statistics
make reset        # Reset database (clear submissions)
make install      # Install dependencies
make help         # Show this help message
```

