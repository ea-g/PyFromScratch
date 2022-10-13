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


# 2) How much pizza do you have in total in pizzas_small?
total = 0



def sum_a_list(x: List[Union[int, float]]) -> Union[float, int]:
    """
    Sums up all the elements in a given list

    :param x:
        list with all numeric elements
    :return:
        the total of the input list, float or integer
    """
    # Fill in the method for summing a list here!
    pass





