import random
import math


def __partition(list, l, r):
    '''Uses random pivot'''
    pivot_index = math.floor(random.random() * (r - l + 1) + l)
    list[r], list[pivot_index] = list[pivot_index], list[r]
    # pivot is at the end of the list
    pivot = list[r]
    smallest = l

    for i in range(l, r):
        if list[i] < pivot:
            list[smallest], list[i] = list[i], list[smallest]
            smallest += 1

    list[smallest], list[r] = list[r], list[smallest]
    return smallest


def __quick_sort(list, l, r):
    if l < r:
        p = __partition(list, l, r)
        __quick_sort(list, l, p - 1)
        __quick_sort(list, p + 1, r)


def quick_sort(list):
    '''Modifies "list" argument'''
    if list is not None and len(list) > 1:
        __quick_sort(list, 0, len(list) - 1)
