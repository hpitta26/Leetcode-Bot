"""Logging configuration"""

import logging
from pathlib import Path
from datetime import datetime


class CustomFormatter(logging.Formatter):
    """Custom formatter with colored output and symbols"""
    
    # ANSI color codes
    COLORS = {
        'SUCCESS': '\033[92m',  # Green
        'ERROR': '\033[91m',    # Red
        'START': '\033[94m',    # Blue
        'COMPLETE': '\033[95m', # Magenta
        'INFO': '\033[96m',     # Cyan
        'WARNING': '\033[93m',  # Yellow
        'RESET': '\033[0m'      # Reset
    }
    
    SYMBOLS = {
        'SUCCESS': '✓',
        'ERROR': '✗',
        'START': '▶',
        'COMPLETE': '☑',
        'INFO': '•',
        'WARNING': '⚠'
    }
    
    def format(self, record):
        # Get the log level name
        levelname = record.levelname
        
        # Determine symbol, color, and label
        if hasattr(record, 'log_type'):
            log_type = record.log_type.upper()
            symbol = self.SYMBOLS.get(log_type, '•')
            color = self.COLORS.get(log_type, self.COLORS['RESET'])
            label = record.log_type.lower()
        else:
            symbol = self.SYMBOLS.get(levelname, '•')
            color = self.COLORS.get(levelname, self.COLORS['RESET'])
            label = levelname.lower()
        
        # Format message with underlined colored label and consistent spacing
        message = record.getMessage()
        underline = '\033[4m'  # ANSI underline
        # Apply color and underline to text only, then add padding spaces
        label_with_underline = f"{color}{underline}{label}\033[0m"
        padding = ' ' * (10 - len(label))
        formatted = f"{color}{symbol}\033[0m {label_with_underline}{padding} {message}"
        
        return formatted


def setup_logger(name: str = "leetcode_bot", log_file: str = "logs/bot.log") -> logging.Logger:
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Prevent duplicate handlers
    if logger.handlers:
        return logger
    
    # Console handler with custom formatter
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(CustomFormatter())
    
    # File handler with standard formatter
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    
    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    # Add custom logging methods
    def log_with_type(level, log_type, message):
        extra = {'log_type': log_type}
        logger.log(level, message, extra=extra)
    
    logger.success = lambda msg: log_with_type(logging.INFO, 'success', msg)
    logger.error_msg = lambda msg: log_with_type(logging.ERROR, 'error', msg)
    logger.start = lambda msg: log_with_type(logging.INFO, 'start', msg)
    logger.complete = lambda msg: log_with_type(logging.INFO, 'complete', msg)
    
    return logger

