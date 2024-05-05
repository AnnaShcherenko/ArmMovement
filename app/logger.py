"""
Customer logger
"""

import logging
import logging.handlers
from datetime import datetime

from termcolor import colored

LOG_FILENAME = "./logs/app.log"
MAX_SIZE_BYTES = 1000000

color_map = {
    logging.DEBUG: "cyan",
    logging.INFO: "green",
    logging.WARNING: "yellow",
    logging.ERROR: "red",
    logging.CRITICAL: "magenta",
}


class ColorLogFormatter(logging.Formatter):
    """
    Formatter for the terminal logs.
    """

    def format(self, record):
        """
        Format log recors using colors.
        """
        color = color_map[record.levelno]
        return (
            colored(f"{record.levelname:10}", color)
            + f"{datetime.now().astimezone().isoformat()} - {record.getMessage()}"
        )


def get_logger(filename: str = "ARM") -> logging.Logger:
    """
    Logger of the project
    """

    my_logger = logging.getLogger(filename)
    if not my_logger.handlers:

        formatter = logging.Formatter(
            "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
        )

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(ColorLogFormatter())
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.flush()

        file_handler = logging.FileHandler(LOG_FILENAME)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.WARNING)
        file_handler.flush()

        my_logger.addHandler(file_handler)
        my_logger.addHandler(stream_handler)
        my_logger.setLevel(logging.DEBUG)

    return my_logger
