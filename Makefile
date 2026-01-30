.PHONY: run leaderboard submissions info reset clear-all install help

PYTHON := python3

run:
	@$(PYTHON) main.py

leaderboard:
	@$(PYTHON) scripts/view_leaderboard.py

submissions:
	@$(PYTHON) scripts/view_submissions.py

info:
	@$(PYTHON) scripts/db_info.py

reset:
	@$(PYTHON) scripts/reset_db.py

install:
	@pip install -r requirements.txt
	@playwright install chromium

help:
	@echo "Available commands:"
	@echo "  make run          - Run the LeetCode bot"
	@echo "  make leaderboard  - View current leaderboard"
	@echo "  make submissions  - View all submissions"
	@echo "  make info         - Show database statistics"
	@echo "  make reset        - Reset database (clear submissions)"
	@echo "  make install      - Install dependencies"
	@echo "  make help         - Show this help message"

