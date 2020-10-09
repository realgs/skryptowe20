def merge_sort(arr):
    n = len(arr)
    if n > 1:
        arr = merge(merge_sort(arr[:n // 2]), merge_sort(arr[n // 2:]))
    return arr


def merge(arr1, arr2):
    n = len(arr1) + len(arr2)
    arr = [0] * n

    i, j, k = 0, 0, 0
    while i < len(arr1) and j < len(arr2):
        if arr1[i] < arr2[j]:
            temp = arr1[i]
            i += 1
        else:
            temp = arr2[j]
            j += 1
        arr[k] = temp
        k += 1

    while i < len(arr1):
        arr[k] = arr1[i]
        i += 1
        k += 1

    while j < len(arr2):
        arr[k] = arr2[j]
        j += 1
        k += 1

    return arr
