"""Load and validate configuration"""

import yaml
from pathlib import Path
from typing import Dict, Any


def load_config(config_path: str = "config.yaml") -> Dict[str, Any]:
    with open(config_path, 'r') as file:
        try:
            config = yaml.safe_load(file)
        except yaml.YAMLError as e:
            raise ValueError(f"Error loading configuration: {e}")
        validate_config(config)
    return config


def validate_config(config: Dict[str, Any]) -> bool:
    if not config:
        raise ValueError("Configuration is empty")
    if not config.get("competition"):
        raise ValueError("Competition section is required")
    if not config.get("usernames"):
        raise ValueError("Usernames section is required")
    if not config.get("problems"):
        raise ValueError("Problems section is required")
    if not config.get("scraping"):
        raise ValueError("Scraping section is required")
    return True

