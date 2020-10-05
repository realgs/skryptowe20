# functional and classical approach to merge sort

def __merge(xs, ys):
    if len(xs) == 0:
        return ys
    if len(ys) == 0:
        return xs
    if xs[0] < ys[0]:
        return [xs[0]] + __merge(xs[1:], ys)
    return [ys[0]] + __merge(xs, ys[1:])

def mergesort_func(xs):
    """Returns the sorted array, does not change the input"""
    if len(xs) < 2:
        return xs
    mid = len(xs) // 2
    return __merge(mergesort_func(xs[:mid]), mergesort_func(xs[mid:]))

def mergesort(arr):
    """Sorts the array in place"""
    if len(arr) < 2:
        return

    mid = len(arr) // 2
    l = arr[:mid]
    r = arr[mid:]

    mergesort(l)
    mergesort(r)

    [i, j, k] = [0, 0, 0]

    while i < len(l) and j < len(r):
        if(l[i] < r[j]):
            arr[k] = l[i]
            i += 1
        else:
            arr[k] = r[j]
            j += 1
        k += 1

    while i < len(l):
        arr[k] = l[i]
        i += 1
        k += 1

    while j < len(r):
        arr[k] = r[j]
        j+= 1
        k+= 1