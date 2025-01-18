import multiprocessing
from fib import fib
import time


def multi_method(seq: list, func):
    """Runs a function concurrently across cores

    Args:
        seq (list): the inputs per function call
        func: function to run
    Returns:
        _type_: _description_
    """
    start = time.time()
    p = multiprocessing.Pool()
    print(p.map(func, seq))
    end = time.time()
    return end - start


def sequential_method(seq: list, func):
    """Runs a function sequentially

    Args:
        seq (list): the inputs per function call
        func (_type_): function to run

    Returns:
        _type_: _description_
    """
    start = time.time()
    # TODO: run the function sequentialy for the items in seq
    end = time.time()
    return end - start


if __name__ == "__main__":
    print("Starting multiprocessing run")
    out = multi_method([5, 5, 5], time.sleep)
    print(f"total time: {out}")
    print("Starting sequential run")
    out2 = sequential_method([5, 5, 5], time.sleep)
    print(f"total time: {out2}")
