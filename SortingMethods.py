def checkList(listOfNumbers):
    if not isinstance(listOfNumbers, list):
        return False
    if not all(isinstance(elem, int) or isinstance(elem, float) for elem in listOfNumbers):
        return False
    return True


def bubbleSort(listOfNumbers):
    if not checkList(listOfNumbers):
        return False
    for i in range(len(listOfNumbers)):
        swapped = False
        for j in range(len(listOfNumbers) - i - 1):
            if listOfNumbers[j] > listOfNumbers[j + 1]:
                (listOfNumbers[j], listOfNumbers[j + 1]) = (listOfNumbers[j + 1], listOfNumbers[j])
                swapped = True
        if not swapped:
            return True
    return True


def quickSortR(listOfNumbers, beg, end):
    if beg < end:
        pivot = listOfNumbers[beg]
        border = beg + 1
        index = border

        while index <= end:
            if (listOfNumbers[index] < pivot):
                (listOfNumbers[border], listOfNumbers[index]) = (listOfNumbers[index], listOfNumbers[border])
                border+=1
            index+=1
        border-=1
        (listOfNumbers[border], listOfNumbers[beg]) = (listOfNumbers[beg], listOfNumbers[border])
        quickSortR(listOfNumbers, beg, border-1)
        quickSortR(listOfNumbers, border+1, end)


def quickSort(listOfNumbers):
    if not checkList(listOfNumbers):
        return False
    quickSortR(listOfNumbers, 0, len(listOfNumbers) - 1)
    return True


if __name__ == '__main__':
    bubbleExList = [5, 5, 12.3, -324, 521623, 0.423]
    quickExList = [4231, 35.2, -3255, 2345, -325.533, 35.23]

    bubbleSort(bubbleExList)
    quickSort(quickExList)

    print(bubbleExList)
    print(quickExList)
