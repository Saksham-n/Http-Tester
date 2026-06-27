import logging
import sys
from pathlib import Path
from rich.logging import RichHandler

def setup_logger(debug: bool = False, log_file: str = "pyload.log") -> logging.Logger:
    """
    Sets up the logger with Rich for console output and a standard FileHandler.
    """
    level = logging.DEBUG if debug else logging.INFO

    # Create root logger
    logger = logging.getLogger("pyload")
    logger.setLevel(level)
    
    # Avoid duplicate logs if setup_logger is called multiple times
    if logger.handlers:
        logger.handlers.clear()

    # Console handler using Rich
    console_handler = RichHandler(rich_tracebacks=True, markup=True)
    console_handler.setLevel(level)
    console_format = logging.Formatter("%(message)s")
    console_handler.setFormatter(console_format)

    # File handler
    file_handler = logging.FileHandler(log_file, mode="a")
    file_handler.setLevel(logging.DEBUG) # Always log DEBUG to file
    file_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(file_format)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

logger = logging.getLogger("pyload")
