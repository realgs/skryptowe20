from random import randint


def random_sort(list_to_sort):
    """
    This is random sort function. It can sort every list, but
    it may take lots of time. It is an acceptable way to sort list
    that are max 6/7 elements long.

    **Params**

    :param list_to_sort: list that will be sorted
    :return: sorted list

    :author: Maciej Wasilewski (wasielwski078@gmail.com)
    """
    if not list_to_sort:
        return list_to_sort
    elif len(list_to_sort) == 1:
        return list_to_sort
    elif __is_sorted(list_to_sort):
        return list_to_sort
    while not __is_sorted(list_to_sort):
        list_to_sort = __randomize(list_to_sort)
    return list_to_sort


def __is_sorted(list_to_check):
    """
    This is an extra function that random_sort uses.
    It checks whether given list is sorted ascending.

    **Params**

    :param list_to_check: list that will be investigated
    :return: result - boolean value

    :author: Maciej Wasilewski (wasielwski078@gmail.com)
    """
    for i in range(len(list_to_check)-1):
        if list_to_check[i] > list_to_check[i+1]:
            return False
    return True


def __randomize(original_list):
    """
    This is an extra function that random_sort uses.
    It takes elements from original_list in random order 
    and creates new list from them. That list is then returned.

    **Params**

    :param original_list: list to randomize
    :return: randomized list

    :author: Maciej Wasilewski (wasielwski078@gmail.com)
    """
    new_maybe_sorted_list = []
    original_len = len(original_list)
    while len(new_maybe_sorted_list) != original_len:
        random_idx = randint(0, len(original_list)-1)
        random_elem = original_list.pop(random_idx)
        new_maybe_sorted_list.append(random_elem)
    return new_maybe_sorted_list
