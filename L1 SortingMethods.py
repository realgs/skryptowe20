def bubble_sort(tab):
    for i in range(len(tab)):
        j = len(tab) - 1
        while j > i:
            if tab[j] < tab[j - 1]:
                tmp = tab[j]
                tab[j] = tab[j - 1]
                tab[j - 1] = tmp
            j -= 1


def quick_sort_partition(arr, left, right):
    i = (left - 1)
    pivot = arr[right]
    for j in range(left, right):
        if arr[j] <= pivot:
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[right] = arr[right], arr[i + 1]
    return i + 1


def quick_sort(arr, left, right):
    if len(arr) <= 1:
        return arr
    if left < right:
        pi = quick_sort_partition(arr, left, right)
        quick_sort(arr, left, pi - 1)
        quick_sort(arr, pi + 1, right)