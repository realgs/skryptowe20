#!/usr/bin/python3

def sort(array):

    i = 0
    for key in array:

        j = i - 1

        while j >= 0 and array[j] > key:
            array[j + 1] = array[j]
            j -= 1

        array[j + 1] = key
        i += 1

    return array
