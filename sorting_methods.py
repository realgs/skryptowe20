import random


def swap(my_list, left, right):
    if left != right:
        temp = my_list[left]
        my_list[left] = my_list[right]
        my_list[right] = temp


def partition(my_list, n_from, n_to):
    rnd_int = n_from + random.randint(0, n_to - n_from - 1)
    swap(my_list, n_from, rnd_int)
    value = my_list[n_from]
    idx_bigger = n_from+1
    idx_lower = n_to - 1
    while True:
        while idx_bigger <= idx_lower and my_list[idx_bigger] <= value:
            idx_bigger += 1
        while my_list[idx_lower] > value:
            idx_lower -= 1
        if idx_bigger < idx_lower:
            swap(my_list, idx_bigger, idx_lower)
        if idx_bigger > idx_lower:
            break
    swap(my_list, idx_lower, n_from)
    return idx_lower


def bubble_sort(my_list):
    right_max_index = len(my_list) - 1
    while right_max_index > 0:
        last_checked = 0
        for i in range(right_max_index):
            if my_list[i] > my_list[i+1]:
                swap(my_list, i, i + 1)
                last_checked = i
        right_max_index = last_checked
    return my_list


def quicksort(my_list, start_index=0, end_index=-1):
    if end_index == -1:
        end_index = len(my_list)
    if end_index - start_index > 1:
        partition_variable = partition(my_list, start_index, end_index)
        quicksort(my_list, start_index, partition_variable)
        quicksort(my_list, partition_variable + 1, end_index)
    return my_list
