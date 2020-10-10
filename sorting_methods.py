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


def heapsort(array):
    if len(array) > 1:
        build_max_heap(array)

        for last_leaf_index in range(len(array) - 1, 0, -1):
            array[0], array[last_leaf_index] = array[last_leaf_index], array[0]
            build_heap_from_index(array, 0, last_leaf_index)


def build_max_heap(array):
    for i in range(len(array) // 2, -1, -1):
        build_heap_from_index(array, i, len(array))


def build_heap_from_index(array, index, last_leaf_index):
    left_child_index = index * 2 + 1
    right_child_index = index * 2 + 2

    if right_child_index < last_leaf_index and array[right_child_index] > array[index]:
        if array[left_child_index] > array[right_child_index]:
            array[index], array[left_child_index] = array[left_child_index], array[index]
            build_heap_from_index(array, left_child_index, last_leaf_index)
        else:
            array[index], array[right_child_index] = array[right_child_index], array[index]
            build_heap_from_index(array, right_child_index, last_leaf_index)

    elif left_child_index < last_leaf_index and array[left_child_index] > array[index]:
        array[index], array[left_child_index] = array[left_child_index], array[index]
        build_heap_from_index(array, left_child_index, last_leaf_index)
