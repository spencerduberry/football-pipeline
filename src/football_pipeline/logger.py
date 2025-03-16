import functools
from collections.abc import Callable


def log_func(func: Callable) -> Callable:
    """Decorator function that prints input/output of logger functions.

    Args:
        func: The function that the input/output will be logged for.

    Returns:
        Callable: Wrapper of the original function with the args and kwargs, then the function's result.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(
            {
                "func": func.__name__,
                "args": args,
                "kwargs": kwargs,
            }
        )

        res = func(*args, **kwargs)

        print(
            {
                "func": func.__name__,
                "res": res,
            }
        )

    return wrapper
