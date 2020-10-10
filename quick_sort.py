import random


def quick_sort(array):
    if len(array) > 1:
        __sort(array, 0, len(array) - 1)


def __sort(array, begin, end):
    pivot = array[random.randint(begin, end)]
    left_index = begin
    right_index = end

    while left_index <= right_index:
        while array[left_index] < pivot:
            left_index += 1
        while array[right_index] > pivot:
            right_index -= 1

        if left_index <= right_index:
            array[left_index], array[right_index] = array[right_index], array[left_index]
            left_index += 1
            right_index -= 1

    if right_index > begin:
        __sort(array, begin, right_index)
    if left_index < end:
        __sort(array, left_index, end)
