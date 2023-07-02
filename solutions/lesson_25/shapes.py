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
        return self.length * self.width

    def perimeter(self):
        return (self.length + self.width) * 2


class Square(Rectangle):
    def __init__(self, length: int | float):
        super().__init__(length, length)


class Cube(Square):
    def volume(self):
        return super().area() * self.length

    def surface_area(self):
        return super().area() * 6
