import time
import asyncio
from contextlib import ContextDecorator
from typing import Callable


class Timer(ContextDecorator):
    def __init__(self, txt: str, unit: str = "seconds", log_func: Callable = print):
        self.txt_ = txt
        self.unit = unit
        self.log_func_ = log_func
        self.execution_time_str = f"0 {unit}"

    def __enter__(self):
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, *exc_info):
        self.end_time = time.perf_counter()
        self.show_timespan(self.start_time, self.end_time)

    def show_timespan(self, start_time: float, end_time: float) -> None:
        time_span = end_time - start_time
        timespan_dict = {
            "seconds": time_span,
            "milliseconds": time_span * 1000,
            "minutes": time_span / 60,
        }
        execution_time = timespan_dict.get(self.unit)
        self.execution_time_str = f"{execution_time:.3f} {self.unit}"
        self.log_func_(f'"{self.txt_}" costs: {self.execution_time_str}')

    def __call__(self, func: Callable):
        def wrapper(*args, **kwargs):
            if asyncio.iscoroutinefunction(func):
                return time_counter_async(func, *args, **kwargs)
            else:
                return time_counter_sync(func, *args, **kwargs)

        def time_counter_sync(func: Callable, *args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            self.show_timespan(start_time, end_time)
            return result

        async def time_counter_async(func: Callable, *args, **kwargs):
            start_time = time.perf_counter()
            result = await func(*args, **kwargs)
            end_time = time.perf_counter()
            self.show_timespan(start_time, end_time)
            return result

        return wrapper


if __name__ == "__main__":
    from pyutils.log4py import logger

    def my_sync_function1():
        time.sleep(2)

    async def my_async_function1():
        await asyncio.sleep(2)

    # context manager
    with Timer(txt="sync task1", unit="milliseconds"):
        my_sync_function1()

    with Timer(txt="async task1", unit="milliseconds", log_func=logger.warning):
        asyncio.run(my_async_function1())

    # decorator
    @Timer(txt="sync task2", unit="milliseconds")
    def my_sync_function2():
        time.sleep(2)

    @Timer(txt="async task2", unit="milliseconds", log_func=logger.info)
    async def my_async_function2():
        await asyncio.sleep(2)

    my_sync_function2()
    asyncio.run(my_async_function2())
