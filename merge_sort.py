import math


def __merge(L, R):
    res = []
    while len(L) > 0 and len(R) > 0:
        if(L[0] > R[0]):
            res.append(R[0])
            R.pop(0)
        else:
            res.append(L[0])
            L.pop(0)

    for e in L:
        res.append(e)

    for e in R:
        res.append(e)

    return res


def __split(list):
    if len(list) > 1:
        m = math.floor(len(list) / 2)
        L = list[:m]
        R = list[m:]
        return L, R
    return list, []


def merge_sort(list):
    '''Returns copy of the argument "list"'''
    if list is not None and len(list) > 1:
        L, R = __split(list)
        return __merge(merge_sort(L), merge_sort(R))
    return list
