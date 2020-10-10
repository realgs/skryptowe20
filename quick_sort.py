import random


def quick_sort(list_to_sort):
    """
    This is quick sort function. This is wrapper function for
    recursive __quick_quick function which makes all of work in this 
    sorting method.

    **Params**

    :param list_to_sort: list that will be sorted
    :return: sorted list

    :author: Maciej Wasilewski (wasielwski078@gmail.com)
    """
    if not list_to_sort:
        return list_to_sort
    __quick_quick(list_to_sort, 0, len(list_to_sort) - 1)
    return list_to_sort


def __quick_quick(list_to_sort, left, right):
    """
    This is function that divides and conquers (a.k.a sort) given list
    until every element is on proper position -> until whole list is sorted.

    **Params**

    :param list_to_sort: list that will be divided and conquered

    :author: Maciej Wasilewski (wasielwski078@gmail.com)
    """
    left_index = left
    right_index = right

    pivot = random.choice(list_to_sort[left:right+1])

    while True:
        while list_to_sort[left_index] < pivot:
            left_index += 1

        while pivot < list_to_sort[right_index]:
            right_index -= 1

        if left_index <= right_index:
            list_to_sort[left_index], list_to_sort[right_index] = list_to_sort[right_index], list_to_sort[left_index]
            left_index += 1
            right_index -= 1

        if left_index > right_index:
            break

    if left < right_index:
        __quick_quick(list_to_sort, left, right_index)
    if left_index < right:
        __quick_quick(list_to_sort, left_index, right)
