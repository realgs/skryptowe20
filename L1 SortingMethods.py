def bubble_sort(tab):
    for i in range(len(tab)):
        j = len(tab) - 1
        while j > i:
            if tab[j] < tab[j - 1]:
                tmp = tab[j]
                tab[j] = tab[j - 1]
                tab[j - 1] = tmp
            j -= 1
    return tab


def quick_sort_partition(arr, low, high):
    i = (low - 1)
    pivot = arr[high]
    for j in range(low, high):
        if arr[j] <= pivot:
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def quick_sort(arr, low, high):
    if len(arr) == 1:
        return arr
    if low < high:
        pi = quick_sort_partition(arr, low, high)
        quick_sort_partition(arr, low, pi - 1)
        quick_sort_partition(arr, pi + 1, high)