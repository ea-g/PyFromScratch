from math import pi
from typing import Union


def area_triangle(h: Union[float, int], b: Union[float, int]) -> float:
    """
    Calculates the area of a triangle following 1/2*b*h.

    :param h:
        Length of the height of the triangle
    :param b:
        Length of the base of the triangle
    :return:
        The area of the triangle
    """
    return 0.5 * h * b


def area_circle(r: Union[float, int]) -> float:
    """
    Calculates the area of a circle following pi*r^2.

    :param r:
        The radius of the circle.
    :return:
        The area of the circle.
    """
    return pi * r ** 2

