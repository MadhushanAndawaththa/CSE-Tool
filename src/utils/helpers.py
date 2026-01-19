"""
Utility functions and configuration loader for CSE Stock Analyzer.
"""

import yaml
import os
from pathlib import Path


def load_config():
    """Load configuration from config.yaml file."""
    config_path = Path(__file__).parent.parent.parent / 'config.yaml'
    
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        return config
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found at {config_path}")
    except yaml.YAMLError as e:
        raise ValueError(f"Error parsing configuration file: {e}")


def format_currency(amount, currency='LKR'):
    """Format amount as currency with thousands separator."""
    return f"{currency} {amount:,.2f}"


def format_percentage(value, decimal_places=2):
    """Format decimal value as percentage."""
    return f"{value * 100:.{decimal_places}f}%"


def validate_positive_number(value, name):
    """Validate that a value is a positive number."""
    if not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a number")
    if value <= 0:
        raise ValueError(f"{name} must be positive")
    return True


def validate_non_negative_number(value, name):
    """Validate that a value is a non-negative number."""
    if not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a number")
    if value < 0:
        raise ValueError(f"{name} must be non-negative")
    return True


def color_text(text, color='green'):
    """Return colored text for terminal output."""
    try:
        from colorama import Fore, Style, init
        init(autoreset=True)
        
        colors = {
            'green': Fore.GREEN,
            'red': Fore.RED,
            'yellow': Fore.YELLOW,
            'blue': Fore.BLUE,
            'cyan': Fore.CYAN,
            'magenta': Fore.MAGENTA,
        }
        
        return f"{colors.get(color, Fore.WHITE)}{text}{Style.RESET_ALL}"
    except ImportError:
        return text


def get_data_dir():
    """Get the data directory path."""
    data_dir = Path(__file__).parent.parent.parent / 'data'
    data_dir.mkdir(exist_ok=True)
    return data_dir
