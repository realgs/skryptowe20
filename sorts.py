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


def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j+1] = arr[j]
            j -= 1

        arr[j+1] = key

    return arr


array_1 = [2, 1, 1, 5, 81, 2, 19]
array_2 = [13.4, 9.8, 8.7, 11.2, 92.9, 54.4, 11.2]

print('Sorted array with quicksort:')
print(quick_sort(array_1, 0, len(array_1)-1))
print('Sorted array with insertionsort')
print(insertion_sort(array_2))
