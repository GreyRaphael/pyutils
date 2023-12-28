import os
import logging
from logging import handlers


def setup_logger(log_name=__name__, level=logging.INFO, log_dir="log"):
    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger(log_name)
    logger.setLevel(level)  # set level for all handler

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s")

    file_handler = handlers.TimedRotatingFileHandler(filename=f"{log_dir}/{log_name}", when="midnight", encoding="utf8")
    # file_handler = handlers.TimedRotatingFileHandler(filename=f"{log_dir}/{log_name}", when="s", interval=10, encoding="utf8", backupCount=30)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger


"""
Usage: setup log_name, level, log_dir in this file, then just import

from mylogger import logger

logger.debug('msg')
logger.info('msg')
logger.warning('msg')
logger.error('msg')
"""

logger = setup_logger(level=logging.DEBUG)
# logger = setup_logger("dailyEval", level=logging.DEBUG, log_dir="log_dir")
