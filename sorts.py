def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i+1], arr[high] = arr[high], arr[i+1]

    return i+1


def quick_sort(arr, low, high):
    if low < high:
        index = partition(arr, low, high)
        quick_sort(arr, low, index-1)
        quick_sort(arr, index+1, high)

    return arr


array_1 = [2, 1, 1, 5, 81, 2, 19]

print('Sorted array with quicksort:')
print(quick_sort(array_1, 0, len(array_1)-1))
