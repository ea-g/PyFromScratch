from solutions.lesson_22.funcs import *


def test_sum():
    a = my_sum([1, 2, 3])
    b = sum([1, 2, 3])
    assert a == b, f'my_sum result, {a}, did not match {b}'
    assert (type(a) is float) or (type(a) is int), f'{type(a)} is not a float or int!'


def test_sum_fail():
    assert my_sum([1, 2]) == 4, f'An intentional failure!'


def test_super_string():
    # some example tests for super_string()
    assert super_string(["hello ", "chicken ",
                         "nugget!"]) == "hello chicken nugget!", f'Failed with iterable of strings, output:{super_string(["hello ", "chicken ", "nugget!"])}'
    assert super_string([1, 2, 3]) == "123", f'Failed with iterable of ints, output: {super_string([1, 2, 3])}'
    assert super_string([1.1, 2.2]) == "1.12.2", f'Failed with iterable of floats, output: {super_string([1.1, 2.2])}'
    assert super_string([0, "hello", 1.3]) == "0hello1.3", "Failed mixed types!"
