from functools import wraps, update_wrapper
from typing import Callable
from queue import Queue


def limit_concurrency(max_concurrent_calls: int):
    q=Queue()
    count=0
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args,**kwargs):
            nonlocal count, q
            if count>=max_concurrent_calls:
                q.put((func,args,kwargs))
                return
            count+=1
            func(*args, **kwargs)
            while not q.empty():
                next_func, next_args, next_kwargs = q.get()
                next_func(*next_args, **next_kwargs)
            count-=1
        return wrapper
    return decorator 


"""
from threading import Lock

def _limit_concurrency(max_concurrent_calls):
    # create a lock to protect the counter
    lock = Lock()

    # initialize the counter and queue
    counter = 0
    queue = Queue()

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal counter
            print('a')
            # if the counter is at the limit, add the request to the queue
            if counter >= max_concurrent_calls:
                queue.put((func, args, kwargs))
                return

            # otherwise, increment the counter and call the function
            with lock:
                counter += 1

            try:
                result = func(*args, **kwargs)
            finally:
                # when the function returns, decrement the counter and process the next request in the queue
                with lock:
                    counter -= 1
                    if not queue.empty():
                        next_func, next_args, next_kwargs = queue.get()
                        next_func(*next_args, **next_kwargs)

            return result
        return wrapper
    return decorator

def __limit_concurrency(max_concurrent_calls: int):
    q = Queue()
    count = 0

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args,**kwargs):
            while not q.empty():
                func, args, kwargs = q.get()
                func(*args, **kwargs)

            nonlocal count
            if count >= max_concurrent_calls:
                q.put((func, args, kwargs))
                return

            count += 1
            result = func(*args, **kwargs)
            count -= 1
            return result

        return wrapper

    return decorator"""