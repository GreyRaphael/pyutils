import os
import logging
from logging import handlers


def get_logger(log_name=__name__, log_dir="log", level=logging.DEBUG):
    os.makedirs(log_dir, exist_ok=True)

    # check logger existence
    if logging.Logger.manager.loggerDict.get(log_name):
        return logging.getLogger(log_name)

    # not exist, new a logger
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
Example: import and use

from log4py import get_logger
logger=get_logger("log_name", "log_dir")

logger.debug('msg')
logger.info('msg')
logger.warning('msg')
logger.error('msg')
"""

if __name__ == "__main__":
    logger = get_logger(level=logging.DEBUG)
    logger = get_logger("dailyEval", "log_dir")
