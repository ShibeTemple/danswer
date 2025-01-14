import time
from collections.abc import Callable
from collections.abc import Generator
from collections.abc import Iterator
from functools import wraps
from typing import Any
from typing import cast
from typing import TypeVar

from danswer.utils.logger import setup_logger

logger = setup_logger()

F = TypeVar("F", bound=Callable)
FG = TypeVar("FG", bound=Callable[..., Generator | Iterator])


def log_function_time(func_name: str | None = None) -> Callable[[F], F]:
    def decorator(func: F) -> F:
        @wraps(func)
        def wrapped_func(*args: Any, **kwargs: Any) -> Any:
            start_time = time.time()
            result = func(*args, **kwargs)
            elapsed_time = time.time() - start_time
            logger.info(f"{func_name or func.__name__} took {elapsed_time} seconds")
            return result

        return cast(F, wrapped_func)

    return decorator


def log_generator_function_time(func_name: str | None = None) -> Callable[[FG], FG]:
    def decorator(func: FG) -> FG:
        @wraps(func)
        def wrapped_func(*args: Any, **kwargs: Any) -> Any:
            start_time = time.time()
            gen = func(*args, **kwargs)
            try:
                value = next(gen)
                while True:
                    yield value
                    value = next(gen)
            except StopIteration:
                pass
            finally:
                elapsed_time = time.time() - start_time
                logger.info(f"{func_name or func.__name__} took {elapsed_time} seconds")

        return cast(FG, wrapped_func)

    return decorator
