import logging
import os
import sys
from datetime import datetime

from colorama import Fore, Style, init

# Define a global formatter that can be used everywhere
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


# Initialize colorama
init(autoreset=True)


class ColoredFormatter(logging.Formatter):
    def format(self, record):
        message = super().format(record)
        if record.levelno == logging.DEBUG:
            return f"{Fore.BLUE}{message}{Style.RESET_ALL}"
        if record.levelno == logging.WARNING:
            return f"{Fore.YELLOW}{message}{Style.RESET_ALL}"
        if record.levelno == logging.CRITICAL or record.levelno == logging.ERROR:
            return f"{Fore.RED}{message}{Style.RESET_ALL}"
        if record.name == "root":  # Only color info messages from this script green
            return f"{Fore.GREEN}{message}{Style.RESET_ALL}"
        return message


def setup_logging(default_level=logging.INFO, log_dir=None):
    """
    Configure logging globally for the entire application.

    Parameters:
        default_level (int): Default logging level
        log_dir (str): Directory to store log files, if None logs to console only
    """
    # Create root logger and set its level
    root_logger = logging.getLogger()
    root_logger.setLevel(default_level)

    # Clear any existing handlers
    if root_logger.handlers:
        root_logger.handlers = []

    # Create formatter
    formatter = ColoredFormatter(LOG_FORMAT, DATE_FORMAT)

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # Create file handler if log_dir is provided
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(log_dir, f"ngen_cal_{timestamp}.log")

        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)


def get_logger(name):
    """
    Get a logger with the specified name.

    Parameters:
        name (str): Logger name

    Returns:
        logging.Logger: Logger instance
    """
    return logging.getLogger(name)
