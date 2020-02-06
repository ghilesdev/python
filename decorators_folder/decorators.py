import functools
import time
import math


def do_twice(func):
    @functools.wraps(func)# Without this line, decorated function's signatures would be overwritten by decorator signature
    def wrapper(*args, **kwargs):#taking arguments : none or multiple
        func(*args, **kwargs)
        return func(*args, **kwargs)
    return wrapper




def decorator(func):
    """
    template:
    :param func:
    :return:
    """
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        #do somethong
        value=func(*args, **kwargs)
        return value
    return wrapper_decorator


def timer(func):
    """
    print the runtime of the function
    :param func:
    :return:
    """
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time=time.perf_counter()
        value=func(*args, **kwargs)
        end_time=time.perf_counter()
        runtime=end_time-start_time
        print(f'finished {func.__name__!r} with a runtime of {runtime:4f} sec')
        return value
    return wrapper_timer


def debug(func):
    """
     print the functions signature and return value:
    :param func:
    :return:
    """
    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr=[repr(a) for a in args]
        kwargs_repr=[f'{k}={v!r}' for k, v in kwargs.items()]
        signatur=', '.join(args_repr + kwargs_repr)
        print(f'calling {func.__name__} ({signatur})')
        value=func(*args, **kwargs)
        print(f'{func.__name__!r} returned {value!r}')
        return value
    return wrapper_debug


def slow_down(func):
    """
    sleeps 1 second before calling the function
    :param func:
    :return:
    """
    @functools.wraps(func)
    def wrapper_slow_down(*args, **kwargs):
        time.sleep(1)
        return func(*args, **kwargs)

    return wrapper_slow_down




