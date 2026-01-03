import logging
from logging.handlers import RotatingFileHandler
import os

LOGGER_NAME = "movie_rating"

def setup_logging():
    if not os.path.exists("logs"):
        os.makedirs("logs")

    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    file_handler = RotatingFileHandler(
        "logs/movie_rating.log",
        maxBytes=1_000_000,
        backupCount=5
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    if not logger.hasHandlers():
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
