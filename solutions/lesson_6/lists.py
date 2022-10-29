from AreaCalculator import *
import random
from typing import List, Union
from timeit import default_timer

#################################################
# SETUP
#################################################
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

#####################################################################################################################

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


def mean_of_list(x: List[Union[int, float]]) -> Union[int, float]:
    """
    Finds the mean of a list of numeric items
    
    :param x:
        a list of ints or floats
    :return:
        the mean of the input list (int, float)
    """
    # fill in the calculation for mean here!
    return sum_a_list(x)/len(x)


def min_of_list(x: List[Union[int, float]]) -> Union[int, float]:
    """
    Finds the minimum value of a list of numeric items and returns it.
    
    :param x:
        a list of ints or floats
    :return:
        the minimum of the input list
    """
    # fill in the method for getting the minimum here!
    output = None
    for xi in x:
        if not output:
            output = xi
        else:
            if xi < output:
                output = xi
    return output


def max_of_list(x: List[Union[int, float]]) -> Union[int, float]:
    """
    Finds the maximum value of a list of numeric items and returns it.

    :param x:
        a list of ints or floats
    :return:
        the maximum of the input list
    """
    output = None
    for xi in x:
        if not output:
            output = xi
        else:
            if xi > output:
                output = xi
    return output


# 4) Who has the biggest pizza slice in slices_big? Who has the smallest?
# What's the average slice size?

a = []
for xi in slices_big:
    b = area_triangle(xi[0], xi[1])
    a.append(b)

biggest = max_of_list(a)
smallest = min_of_list(a)
average = mean_of_list(a)

print(f'{names[a.index(biggest)]} has the largest slice at {biggest:.2f} square cm.')
print(f'{names[a.index(smallest)]} has the smallest slice at {smallest:.2f} square cm.')
print(f'{average:.2f} square cm is the mean pizza slice size. Huuuuge!')
    


