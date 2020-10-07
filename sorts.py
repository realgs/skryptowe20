def insertSort(array):

    for i in range(1, len(array)):
        current = array[i]
        j = i-1
        while j >= 0 and current < array[j] :
                array[j+1] = array[j]
                j -= 1
        array[j+1] = current


def partition(array, start, end):
    pivot = array[start]
    low = start + 1
    high = end

    while True:
        while low <= high and array[high] >= pivot:
            high = high - 1

        while low <= high and array[low] <= pivot:
            low = low + 1

        if low <= high:
            array[low], array[high] = array[high], array[low]
        else:
            break

    array[start], array[high] = array[high], array[start]

    return high



def quickSort(array, start, end):
    if start >= end:
        return

    p = partition(array, start, end)
    quickSort(array, start, p-1)
    quickSort(array, p+1, end)


arr = [12, 101, 13, 5, 6]
arr2 = [12, 51, 1333, 5, 16]
insertSort(arr)
quickSort(arr1,0,len(arr)-1)
print(arr)
print(arr2)
