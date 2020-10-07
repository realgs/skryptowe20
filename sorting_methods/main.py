#!/usr/bin/python3

from algorithms import *
import random

SIZE = 100
# array = [292, 1, 2, 20, 15, 10, 2, 2, 1, 4, 100, 7, 0]

def generate_random_array(size):
    array = []
    for x in range(size): array.append(random.randint(0, size))
    return array


if __name__ == "__main__":
    array = generate_random_array(SIZE)
    print("b4:", array)
    print("\ninsert:", insert.sort(array.copy()))
    print("\nquick:", quick.sort(array.copy()))
