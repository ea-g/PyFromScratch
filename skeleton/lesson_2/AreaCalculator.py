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


def main() -> bool:
    """
    UI for the area calculator. Prompts the user to choose which shape to calculate the area of and the relevant
    parameters.

    :return:
        bool, to run the program again or not.
    """
    shape = input("Which shape do you need the area of, a circle or a triangle? ")
    another = False

    # TODO:
    # In the space below, make the main logic of our app. That is, what should we do if the user inputs "circle"? What
    # about "triangle"? What if they enter something else?
    if shape.lower() == 'circle':
        # program here!
        pass
    elif shape.lower() == 'triangle':
        # prompt for triangle here
        pass
    else:
        # what if we don't get triangle or circle?
        pass

    # Last we should ask the user if we want to do a different shape or input (run the program again).
    # change "another" to user input!
    another = input("Do you want to run this again? y/n ")
    if another == 'y':
        pass
    else:
        pass
    return another


if __name__ == "__main__":
    again = 1
    while again:
        again = main()
