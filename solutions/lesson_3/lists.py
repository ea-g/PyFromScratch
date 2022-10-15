from AreaCalculator import *
import random
from typing import List, Union

##############################################################
# SETUP
##############################################################

# lists we'll use today
pizzas_small = [4, 7, 12, 40, 3, 88, 60]
slices_small = [[12, 5], [0.5, 80], [3, 30], [1000, 0.1], [13, 13]]
names_small = ['Leo', 'Pikachu', 'Maria', 'Ironman', 'Dan Carter']

###################################################################################################

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
    # Fill in the method for summing a list here!
    pass






