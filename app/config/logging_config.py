import logging
import ecs_logging
import os


LOG_FILE = os.getenv("LOG_FILE", "app.log")


def setup_logging():
    log_handler = logging.FileHandler(LOG_FILE)
    log_handler.setFormatter(ecs_logging.StdlibFormatter())
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(log_handler)
