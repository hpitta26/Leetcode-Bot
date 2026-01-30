.PHONY: set-comp run revert-run comp-status leaderboard submissions info reset install help

PYTHON := python3

set-comp:
	@$(PYTHON) scripts/set_comp.py

run:
	@$(PYTHON) main.py

revert-run:
	@$(PYTHON) scripts/revert_run.py

comp-status:
	@$(PYTHON) scripts/comp_status.py

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
	@echo "  make set-comp     - Set up a new competition from config"
	@echo "  make run          - Run the LeetCode bot"
	@echo "  make revert-run   - Revert run (clears submissions, allows re-run)"
	@echo "  make comp-status  - Show current competition status"
	@echo "  make leaderboard  - View current leaderboard"
	@echo "  make submissions  - View all submissions"
	@echo "  make info         - Show database statistics"
	@echo "  make reset        - Reset database (clear submissions)"
	@echo "  make install      - Install dependencies"
	@echo "  make help         - Show this help message"

