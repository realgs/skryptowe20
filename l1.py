def quicksort(toSort):
    if toSort is None:
        return toSort
    elif len(toSort) > 1:
        return __quicksort(toSort.copy(), 0, len(toSort) - 1)
    else:
        return toSort.copy()

    
def __quicksort(toSort, leftIndex, rightIndex):
    index = __partition(toSort, leftIndex, rightIndex)
    if leftIndex < index - 1:
        __quicksort(toSort, leftIndex, index - 1)
    if index < rightIndex:
        __quicksort(toSort, index, rightIndex)
    return toSort

def __partition(toSort, leftIndex, rightIndex):
    i = leftIndex
    j = rightIndex
    pivot = toSort[(leftIndex + rightIndex) // 2]
    while i <= j:
        while toSort[i] < pivot:
            i = i + 1
        while toSort[j] > pivot:
            j = j - 1
        if i <= j:
            toSort[i], toSort[j] = toSort[j], toSort[i]
            i = i + 1
            j = j - 1
    return i

def mergesort(toSort):
    if toSort is None:
        return toSort
    else:
        return __mergesort(toSort.copy())

def __mergesort(toSort):
    if len(toSort) > 1:
        middleIndex = len(toSort) // 2
        leftPart = toSort[:middleIndex]
        rightPart = toSort[middleIndex:]
        leftPart = __mergesort(leftPart)
        rightPart = __mergesort(rightPart)
        result = __merge(leftPart, rightPart, toSort)
        return result
    else:
        return toSort

def __merge(first, second, result):
   firstIndex = 0
   firstLength = len(first)
   secondIndex = 0
   secondLength = len(second)
   resultIndex = 0
   while True:
        if firstIndex >= firstLength:
            __appendRemaining(second, result, secondIndex, resultIndex)
            return result
        if secondIndex >= secondLength:
            __appendRemaining(first, result, firstIndex, resultIndex)
            return result

        if first[firstIndex] <= second[secondIndex]:
            result[resultIndex] = first[firstIndex]
            firstIndex = firstIndex + 1
        else:
            result[resultIndex] = second[secondIndex]
            secondIndex = secondIndex + 1
        resultIndex = resultIndex + 1

def __appendRemaining(src, dest, srcStartIndex, destStartIndex):
    srcLength = len(src)
    destIndex = destStartIndex
    srcIndex = srcStartIndex
    while srcIndex < srcLength:
        dest[destIndex] = src[srcIndex]
        srcIndex = srcIndex + 1
        destIndex = destIndex + 1

def runTest(testArray, testMsg):
    print(testMsg)
    print("Tablica przed posortowaniem {0}".format(testArray))
    print("Tablica po posortowaniu quicksortem {0}".format(quicksort(testArray)))
    print("Tablica po posortowaniu mergesortem {0}".format(mergesort(testArray)))
    print("---")
       
if __name__ == "__main__":
    runTest([2, 3, 5, 10, 200], "Test dla posortowanej tablicy")
    runTest([30, 7, 5, 2, 1], "Test dla tablicy posortowanej odwrotnie")
    runTest([3, 3, 3, 3, 3, 3], "Test dla tablicy identycznych elementów")
    runTest([-1, -100, -2, -30, -81], "Test dla wartości ujemnych")
    runTest([290], "Test dla tablicy jednoelementowej")
    runTest([], "Test dla pustej tablicy")
    runTest(None, "Test dla nulla")
