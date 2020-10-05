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


print('insertion sort: ', insertionSort([0, -1, 0, 9.2, 12, -22.5, 3, 9.9]))
