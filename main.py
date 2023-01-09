# pylint:disable=missing-function-docstring
# pylint:disable=logging-fstring-interpolation

import logging
import threading
import time
from typing import Any, Callable, Iterable

import requests

HTTP_REQUEST_TIMEOUT = 10
LOG_FORMAT = "%(asctime)s: %(message)s"
DATE_FORMAT = "%H:%M:%S"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)


def timeit(name: str) -> Callable:
    def wrapper(func: Callable) -> Callable:
        def inner(*args: Iterable, **kwargs: Iterable) -> Any:
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            logging.debug(f"[{name}] Execution time = {end - start}")
            return result

        return inner

    return wrapper


@timeit("Network")
def network_call(method: str, url: str, parameters: Iterable) -> None:
    result = requests.request(method, url, params=parameters, timeout=HTTP_REQUEST_TIMEOUT)
    logging.debug(f"Request status OK is {result.ok}")


@timeit("Threads")
def with_threads() -> None:
    thread1 = threading.Thread(target=network_call, args=("GET", "https://www.google.com", None))
    thread2 = threading.Thread(target=network_call, args=("GET", "https://www.google.com", None))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()


@timeit("Linear calls")
def linear_calls() -> None:
    network_call("GET", "https://www.google.com", None)
    network_call("GET", "https://www.google.com", None)


if __name__ == "__main__":
    with_threads()
    linear_calls()
