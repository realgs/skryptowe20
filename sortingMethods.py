def insertionSort(unorderedArr, orderedArr=[]):
    if not unorderedArr:
        return orderedArr
    currentItem = unorderedArr.pop(0)

    def insertItem(array):
        if not array or array[0] >= currentItem:
            return [currentItem] + array
        else:
            return [array[0]] + insertItem(array[1:])

    return insertionSort(unorderedArr, insertItem(orderedArr))


def quickSort(array):
    if len(array) < 2: return array
    pivot = array.pop(0)

    def partition(arr, smaller, bigger):
        if not arr:
            return smaller, bigger
        elif arr[0] <= pivot:
            return partition(arr[1:], smaller + [arr[0]], bigger)
        else:
            return partition(arr[1:], smaller, bigger + [arr[0]])

    smaller, bigger = partition(array, [], [])
    return quickSort(smaller) + [pivot] + quickSort(bigger)


print('insertion sort: ', insertionSort([0, -1, 0, 9.2, 12, -22.5, 3, 9.9]))
print('quick sort: ', quickSort([0, -55.9, -55.8, 9.2, 2, 0, 3.3, 3.3, 9.11]))
