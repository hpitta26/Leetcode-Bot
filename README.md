# LeetCode Competition Bot

A bot that tracks LeetCode problem submissions for competition participants and generates a leaderboard.

## Features

- 🕷️ Scrapes LeetCode user profiles using Playwright
- 📊 Tracks which problems each user has solved
- ⏰ Designed to run via cron (daily updates)
- 💾 Stores data in SQLite database

## Project Structure

```
leetcode-bot/
├── config/              # Configuration files
│   └── config.yaml      # Competition settings, users, problems
├── src/                 # Source code
│   ├── scraper/         # Web scraping logic
│   ├── database/        # Database operations
│   └── utils/           # Utilities (config, logging)
├── data/                # SQLite database (created at runtime)
├── logs/                # Application logs
├── main.py              # Entry point
└── requirements.txt     # Python dependencies
```

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

Edit `config/config.yaml`:
- Add participant usernames
- Add problems to track (with slugs and points)
- Set competition dates

### 3. Run Manually

```bash
python main.py
```

### 4. Setup Cron (Optional)

Run daily at 8 AM:

```bash
# Edit crontab
crontab -e

# Add this line:
0 8 * * * cd /path/to/leetcode-bot && /path/to/venv/bin/python main.py >> logs/cron.log 2>&1
```

## Output

The bot generates:
- `data/competition.db` - SQLite database with all data
- `logs/bot.log` - Application logs

## Configuration

See `config/config.yaml` for all available options.

## Development

This is a skeleton structure - implementation needed for:
- [ ] Playwright scraping logic
- [ ] Database schema and operations
- [ ] Error handling and logging

