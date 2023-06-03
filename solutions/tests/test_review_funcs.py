from solutions.lesson_23_review.review_funcs import *


def test_largest():
    assert largest([1, 2, 3]) == 3
    assert largest(["hello", "chicken", "nugget"]) == "chicken", "fail string"
    assert largest([3.4, 6, "bananas", 1.9, 7.001]) == 7.001, "fail mix"


def test_prob():
    assert prob([1, 1, 1, 2], 1) == 0.75, "Easy test failed!"
    assert prob([], 123) == 0, "empty set failed!"
