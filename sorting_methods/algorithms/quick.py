#!/usr/bin/python3

def sort(array):
    sorting_procedure(0, len(array) - 1, array)
    return array

def sorting_procedure(low, high, array):
    pivot = array[(low + high) // 2]
    i = low
    j = high

    while i <= j:
        while array[i] < pivot: i += 1
        while array[j] > pivot: j -= 1

        if i <= j:
            array[i], array[j] = array[j], array[i]
            i += 1
            j -= 1

    if j > low: sorting_procedure(low, j, array)
    if i < high: sorting_procedure(i, high, array)
