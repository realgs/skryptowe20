def __quick_sort(to_sort: list):
    __quick_sort_fun(to_sort, 0, len(to_sort) - 1)


def __quick_sort_fun(to_sort, first, last):
    if len(to_sort) == 1:
        return to_sort
    if first < last:
        ind = __divide_list(to_sort, first, last)
        __quick_sort_fun(to_sort, first, ind - 1)
        __quick_sort_fun(to_sort, ind + 1, last)


def __divide_list(array, first, last):
    actual_pos = first - 1
    pivot = array[last]
    for i in range(first, last):
        if array[i] <= pivot:
            actual_pos = actual_pos + 1
            __switch_elements(array, i, actual_pos)

    __switch_elements(array, actual_pos + 1, last)
    return actual_pos + 1


def __selection_sort(to_sort:list):
    n = len(to_sort)
    for i in range(n):
        minimal = i
        for j in range(i + 1, n):
            if to_sort[j] < to_sort[minimal]:
                minimal = j

        if to_sort[minimal] != i:
            __switch_elements(to_sort, minimal, i)
    return to_sort


def __switch_elements(array, element_pos, target_pos):
    array[element_pos], array[target_pos] = array[target_pos], array[element_pos]


def sort(to_sort, method="quick"):
    if method == "quick" or method is None:
        __quick_sort(to_sort)
    elif method == "selection":
        __selection_sort(to_sort)


