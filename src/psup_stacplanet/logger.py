import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

LOG_DIR = Path(os.getenv("PSUP_STACPLANET_LOG_DIR", "psup_stacplanet_logs"))
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FORMAT_DETAILLED = "%(asctime)s %(levelname)-8s %(name)s: %(message)s"
LOG_FORMAT_SIMPLE = "%(levelname)s: %(message)s"

LOG_DATE_FORMAT_DETAILLED = "%Y-%m-%d %H:%M:%S"
LOG_DATE_FORMAT_SIMPLE = "[%X]"


def get_logger(name: str) -> logging.Logger:
    """Generates the same logger configuration for all parts of the program

    Args:
        name (str): _description_

    Returns:
        logging.Logger: _description_
    """
    log = logging.getLogger(name)
    log.setLevel(logging.INFO)

    # If configured
    if log.handlers:
        return log

    # Configure handlers - command line
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(
        logging.Formatter(fmt=LOG_FORMAT_SIMPLE, datefmt=LOG_DATE_FORMAT_SIMPLE)
    )
    log.addHandler(console_handler)

    # Configure handlers - file
    file_handler = RotatingFileHandler(
        LOG_DIR / "process.log", maxBytes=5000000, backupCount=3, encoding="utf-8"
    )
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(
        logging.Formatter(fmt=LOG_FORMAT_DETAILLED, datefmt=LOG_DATE_FORMAT_DETAILLED)
    )
    log.addHandler(file_handler)

    log.propagate = False

    return log
