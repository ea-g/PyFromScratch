import numpy as np
import matplotlib.pyplot as plt

# We can represent an array in python with numpy
a = np.array([1, 2, 3, 4])
print(a)

# notice that we can also specify size and fill with ones or zeros:
b = np.ones((10, 10))
c = np.zeros((10, 10))

# we can then visualize our matrices (2D arrays) with matplotlib
plt.matshow(b)
plt.title("Matrix B")
plt.show()

plt.matshow(c)
plt.title("Matrix C")
plt.show()

# TODO: create an array to represent the maze we drew then show it using matplotlib
