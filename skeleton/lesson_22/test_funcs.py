from funcs import *


def test_sum():
    a = my_sum([1, 2, 3])
    b = sum([1, 2, 3])
    assert a == b, f'my_sum result, {a}, did not match {b}'


def test_sum_fail():
    assert my_sum([1, 2]) == 4, f'An intentional failure!'


def test_super_string():
    # TODO: make a test for your super_string() function!
    pass
