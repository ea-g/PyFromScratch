def factorial_base(n: int) -> int:
    """
    Finds n! by multiplying the numbers 1 to n together. Restricted to values n>=0, returning 1 when n=0.

    :param n: int, 0 or greater
    :return: int, result from n!.
    """
    # TODO: implement factorial using a while loop
    if n < 0:
        raise ValueError(f"{n} must be >= 0!")
    if type(n) is not int:
        raise TypeError(f"{n} must be an integer but is type {type(n)}")
    pass


def factorial_recursion(n: int) -> int:
    """
    Finds n! by multiplying the numbers 1 to n together. Restricted to values n>=0, returning 1 when n=0.

    :param n: int, 0 or greater
    :return: int, result from n!.
    """
    # TODO: implement factorial using recursion.
    if n < 0:
        raise ValueError(f"{n} must be >= 0!")
    if type(n) is not int:
        raise TypeError(f"{n} must be an integer but is type {type(n)}")
    pass


def binary_search_recursion(x: list, target, start: int, end:int) -> int | None:
    """
    Searches through the input array for the target and returns the position if found,
    otherwise returns none. Does so using the binary search algorithm (fast)!

    :param x: input array to search through
    :param target: item to find
    :param start: beginning index in the list to search through
    :param end: end index of the list to search through
    :return: position of the item in the array if present
    """
    # TODO: try implementing binary search recursively!
    pass