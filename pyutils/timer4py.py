import time
import asyncio
from typing import Callable


def timer(unit: str = "seconds", log_func: Callable = print):
    """
    timer decorator: 支持sync和async函数的计时
    :param func: function to be timed
    :param unit: time unit
    :return: time_counter
    """

    def decorator(func: Callable):
        def show_timespan(start_time: float, end_time: float) -> None:
            time_span = end_time - start_time
            timespan_dict = {
                "seconds": time_span,
                "milliseconds": time_span * 1000,
                "minutes": time_span / 60,
            }
            execution_time = timespan_dict.get(unit)
            log_func(f'"{func.__name__}" costs: {execution_time:.3f} {unit}')

        def wrapper(*args, **kwargs):
            if asyncio.iscoroutinefunction(func):
                return time_counter_async(func, *args, **kwargs)
            else:
                return time_counter_sync(func, *args, **kwargs)

        def time_counter_sync(func: Callable, *args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            show_timespan(start_time, end_time)
            return result

        async def time_counter_async(func: Callable, *args, **kwargs):
            start_time = time.perf_counter()
            result = await func(*args, **kwargs)
            end_time = time.perf_counter()
            show_timespan(start_time, end_time)
            return result

        return wrapper

    return decorator


if __name__ == "__main__":
    # simple usage
    @timer()
    def my_sync_function():
        # Code to be timed
        time.sleep(2)

    # with parameters
    from log4py import logger

    @timer(unit="milliseconds", log_func=logger.warning)
    async def my_async_function():
        # Code to be timed
        await asyncio.sleep(2)

    my_sync_function()
    asyncio.run(my_async_function())
