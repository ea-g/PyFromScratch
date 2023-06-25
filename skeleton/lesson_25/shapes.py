"""
Working with classes, based upon https://realpython.com/python-super/#an-overview-of-pythons-super-function
"""


class Shape:
    """
    A metaclass for any shape, it provides a template for what we expect any type of shape to have and do.
    """

    def area(self):
        pass

    def perimeter(self):
        pass


class FalseRectangle(Shape):
    length = 5
    width = 10
    chicken = 1000

    def __init__(self, length: int | float, width: int | float):
        self.length -= length
        self.width -= width


class Rectangle(Shape):
    def __init__(self, length: int | float, width: int | float):
        self.length = length
        self.width = width

    def area(self):
        # TODO: implement the area method
        pass

    def perimeter(self):
        # TODO implement the perimeter method
        pass

# TODO:
#  1) Create a class for Squares, which inherits from the Rectangle class.
#  2) Create a class for Cubes which extends and inherits from the Square class. It should have methods for volume
#  and surface area

