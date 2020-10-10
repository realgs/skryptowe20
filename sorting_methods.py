from random import randint


def quicksort(array):
    if len(array) > 1:
        quicksort_helper(array, 0, len(array) - 1)


def quicksort_helper(array, left_bound, right_bound):
    pivot = randint(left_bound, right_bound)
    pivot_value = array[pivot]
    array[pivot], array[right_bound] = array[right_bound], array[pivot]

    left = left_bound
    right = right_bound - 1

    while left <= right:
        if array[left] < pivot_value:
            left += 1
        else:
            while left <= right and array[right] >= pivot_value:
                right -= 1

            if left < right:
                array[left], array[right] = array[right], array[left]

    pivot = left
    array[pivot], array[right_bound] = array[right_bound], array[pivot]

    if left_bound < pivot - 1:
        quicksort_helper(array, left_bound, pivot - 1)

    if right_bound > pivot + 1:
        quicksort_helper(array, pivot + 1, right_bound)
