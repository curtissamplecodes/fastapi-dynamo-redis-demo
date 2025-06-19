import logging
import time
from functools import wraps

logger = logging.getLogger(__name__)

def timing_logger(name: str = ""):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = await func(*args, **kwargs)
            duration = time.perf_counter() - start

            logger.info(f"{name or func.__name__} took {duration:.4f} seconds")
            return result
        return wrapper
    return decorator