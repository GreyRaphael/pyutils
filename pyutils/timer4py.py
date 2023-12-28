import time
import asyncio


def timer(func):
    """
    timer decorator
    :param func: function to be timed
    :return: time_counter
    """

    def wrapper(*args, **kwargs):
        if asyncio.iscoroutinefunction(func):
            return time_counter_async(func, *args, **kwargs)
        else:
            return time_counter_sync(func, *args, **kwargs)

    def time_counter_sync(func, *args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        print(f'"{func.__name__}" costs: {end_time-start_time:.3f} seconds')
        return result

    async def time_counter_async(func, *args, **kwargs):
        start_time = time.perf_counter()
        result = await func(*args, **kwargs)
        end_time = time.perf_counter()
        print(f'"{func.__name__}" costs: {end_time-start_time:.3f} seconds')
        return result

    return wrapper


if __name__ == "__main__":

    @timer
    def my_sync_function():
        # Code to be timed
        time.sleep(2)

    @timer
    async def my_async_function():
        # Code to be timed
        await asyncio.sleep(2)

    my_sync_function()
    asyncio.run(my_async_function())
