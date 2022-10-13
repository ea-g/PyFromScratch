from AreaCalculator import *
import random
from typing import List, Union

# get a list of names
names = []
with open('names.txt', 'r') as f:
    for line in f:
        names.append(line.strip())

# get a big list of pizza slices
random.seed(5)
slices_big = [[random.uniform(0.001, 1000), random.uniform(0.001, 1000)] for i in range(len(names))]

# other lists we'll use
pizzas_small = [4, 7, 12, 40, 3, 88, 60]
slices_small = [[12, 5], [0.5, 80], [3, 30], [1000, 0.1], [13, 13]]
names_small = ['Leo', 'Pikachu', 'Maria', 'Ironman', 'Dan Carter']

# 1) Make a list of the sizes of all pizzas in pizzas_small
areas = []
for p in pizzas_small:
    a = area_circle(p)
    areas.append(a)
    print(areas)

print(areas)

# 2) How much pizza do you have in total in pizzas_small?
t = 0
for p in areas:
    t = t + p
print("Our total pizza area is:")
print(t)


def sum_a_list(x: List[Union[int, float]]) -> Union[float, int]:
    """
    Sums up all the elements in a given list

    :param x:
        list with all numeric elements
    :return:
        the total of the input list, float or integer
    """
    out = 0
    for i in x:
        out += i
    return out

# 3) Who has the biggest pizza slice in slices_small? Who has the smallest?
# What's the average slice size?

slice_area = []
for s in slices_small:
    slice_area.append(area_triangle(s[0], s[1]))

print(slice_area)
print(sum_a_list(slice_area)/len(slice_area))


# 4) Who has the biggest pizza slice in slices_big? Who has the smallest?
# What's the average slice size?

def mean_of_list(x: List[Union[int, float]]) -> Union[int, float]:
    """
    Finds the mean of a list of numeric items
    
    :param x:
        a list of ints or floats
    :return:
        the mean of the input list (int, float)
    """
    # fill in the calculation for mean here!
    pass


def min_of_list(x: List[Union[int, float]]) -> Union[int, float]:
    """
    Finds the minimum value of a list of numeric items and returns it.
    
    :param x:
        a list of ints or floats
    :return:
        the minimum of the input list
    """
    # fill in the method for getting the minimum here!
    pass


def max_of_list(x: List[Union[int, float]]) -> Union[int, float]:
    """
    Finds the maximum value of a list of numeric items and returns it.

    :param x:
        a list of ints or floats
    :return:
        the maximum of the input list
    """
    # fill in the method for getting the maximum here!
    pass




