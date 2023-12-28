# pyutils

- [pyutils](#pyutils)
  - [log4py](#log4py)

## log4py

[Usage Examples](examples/log4py_example.py)

```py
from pyutils.log4py import logger

for i in range(100):
    logger.debug("Debug message %d" % i)
    logger.info("Info message %d" % i)
    logger.warning("Warning message %d" % i)
    logger.error("Error message %d" % i)
```