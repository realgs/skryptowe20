def mergeSort(array):
    if len(array) > 1:
        midIndex = len(array) // 2
        left = mergeSort(array[:midIndex])
        right = mergeSort(array[midIndex:])
        array = []
        i = 0
        j = 0
        while i < len(left) and j < len(right):
            if left[i] > right[j]:
                array.append(right[j])
                j += 1
            else:
                array.append(left[i])
                i += 1
        array += left[i:]
        array += right[j:]
    return array

def combSort(array, shrinkingFactor):
    length = len(array)
    gap = length
    isSwap = True
    while gap != 1 or isSwap:
        gap = int(gap / shrinkingFactor)
        if gap < 1:
            gap = 1
        isSwap = False
        for i in range(length - gap):
            if array[i] > array[i + gap]:
                array[i], array[i + gap] = array[i+gap], array[i]
                isSwap = True
    return array

if __name__ == '__main__':
    arrayToSort = [3, 15, -50, 0, 2.3, 45, 2, 4, 90, 124512, 1234.320, -13.32, -1]
    print(f"List to sort: {arrayToSort}\n")

    combSortArray = combSort(arrayToSort, 1.3)
    print(f"Comb sort array result: {combSortArray}")

    mergeSortArray = mergeSort(arrayToSort)
    print(f"Merge sort array result: {mergeSortArray}")