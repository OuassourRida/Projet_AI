"""Configuration module for backend settings."""
import os
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Data directory
DATA_DIR = PROJECT_ROOT / 'data'

# Debug mode
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

# Server configuration
HOST = os.getenv('FLASK_HOST', '0.0.0.0')
PORT = int(os.getenv('FLASK_PORT', 5000))

# Recommendation defaults
DEFAULT_TOP_K = 10
MAX_TOP_K = 50
MIN_TOP_K = 1

# Logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
