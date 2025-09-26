"""
Logging configuration for the New Jersey Municipal Consolidation Analysis project.
"""

import logging
import logging.config
from pathlib import Path
from config.settings import LOGGING_CONFIG, PROJECT_ROOT


def setup_logging():
    """Setup logging configuration for the project."""
    # Create logs directory
    logs_dir = PROJECT_ROOT / 'logs'
    logs_dir.mkdir(exist_ok=True)
    
    # Configure logging
    logging.config.dictConfig(LOGGING_CONFIG)
    
    # Get root logger
    logger = logging.getLogger()
    logger.info("Logging system initialized")
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for a specific module."""
    return logging.getLogger(name)
