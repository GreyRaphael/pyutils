import os
import sys
import time

# sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from pyutils.log4py import get_logger

logger = get_logger()

for i in range(100):
    logger.debug("Debug message %d" % i)
    logger.info("Info message %d" % i)
    logger.warning("Warning message %d" % i)
    logger.error("Error message %d" % i)
    time.sleep(1)
