from collections import Counter
from random import randint

if __name__ == "__main__":
    my_ints = [randint(0, 100) for i in range(10000)]
    a = Counter(my_ints)
    print(a)