"""
Centralized Logging Configuration.

This module provides a setup function to configure logging for the application,
logging to both a file and the console with appropriate formatting.
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

# Default log format
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def setup_logging(
    log_level: int = logging.INFO,
    log_dir: str = "logs",
    log_file_prefix: str = "cse_analyzer"
) -> None:
    """
    Configure logging for the application.
    
    Args:
        log_level: Logging level (default: logging.INFO)
        log_dir: Directory to store log files
        log_file_prefix: Prefix for log files
    """
    # Create logs directory if it doesn't exist
    log_dir_path = Path(log_dir)
    log_dir_path.mkdir(parents=True, exist_ok=True)
    
    # Generate log filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d")
    log_filename = f"{log_file_prefix}_{timestamp}.log"
    log_path = log_dir_path / log_filename
    
    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format=LOG_FORMAT,
        datefmt=DATE_FORMAT,
        handlers=[
            # File handler
            logging.FileHandler(log_path, encoding='utf-8'),
            # Console handler
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Log startup message
    logging.info(f"Logging initialized. Log file: {log_path}")

def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the specified name.
    
    Args:
        name: Name of the logger (typically __name__)
    
    Returns:
        logging.Logger: Configured logger instance
    """
    return logging.getLogger(name)
