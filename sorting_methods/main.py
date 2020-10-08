#!/usr/bin/python3

from algorithms import *
import random

SIZE = 100

def generate_random_array(size):
    array = []
    for x in range(size): array.append(random.randint(0, size))
    return array

def generate_ascending_array(size):
    return [*range(size)]

def generate_descending_array(size):
    return [*range(size, 0, -1)]


if __name__ == "__main__":
    array = generate_random_array(SIZE)
    print("b4:", array)
    print("\ninsert:", insert.sort(array.copy()))
    print("\nquick:", quick.sort(array.copy()))

    array = generate_ascending_array(SIZE)
    print("\nb4:", array)
    print("\ninsert:", insert.sort(array.copy()))
    print("\nquick:", quick.sort(array.copy()))

    array = generate_descending_array(SIZE)
    print("\nb4:", array)
    print("\ninsert:", insert.sort(array.copy()))
    print("\nquick:", quick.sort(array.copy()))
