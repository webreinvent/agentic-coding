"""
Configuration module for loading environment variables.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Application Settings
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# API Configuration
OPEN_API_KEY = os.getenv("OPEN_API_KEY", "default_key")

# Export configuration as a dictionary for easy access
config = {
    "app": {
        "debug": DEBUG,
        "log_level": LOG_LEVEL
    },
    "openai": {
        "api_key": OPEN_API_KEY,
    },
}
