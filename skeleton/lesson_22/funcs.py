from typing import Iterable


def my_sum(my_iter: Iterable[int | float]):
    start = 0
    for i in my_iter:
        start += i
    return start


def super_string(my_iter: Iterable[int | float | str]) -> str:
    """
    Creates a giant string from an iterable.

    :param my_iter: Iterable with ints, floats, or strings inside
    :return: string containing everything from the input iterable
    """
    # TODO: implement a function that
    #  1) takes each item in an iterable & turns it into a string if necessary
    #  2) adds that new string onto a single 'super' string
    #  3) returns the single string containing all data

    pass
