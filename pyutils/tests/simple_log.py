import os
import sys

# sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from log4py import logger

for i in range(100):
    logger.debug("Debug message %d" % i)
    logger.info("Info message %d" % i)
    logger.warning("Warning message %d" % i)
    logger.error("Error message %d" % i)
