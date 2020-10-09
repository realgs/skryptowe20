def bubbleSort(listOfNumbers):
    if not checkList(listOfNumbers):
        return False
    for i in range(len(listOfNumbers)):
        swapped = False
        for j in range(len(listOfNumbers) - i - 1):
            if listOfNumbers[j] > listOfNumbers[j+1]:
                (listOfNumbers[j], listOfNumbers[j+1]) = (listOfNumbers[j+1], listOfNumbers[j])
                swapped = True
        if not swapped:
            return True
    return True


def quickSort(listOfNumbers):
    pass


def checkList(listOfNumbers):
    if not isinstance(listOfNumbers, list):
        return False
    if not all(isinstance(elem, int) or isinstance(elem, float) for elem in listOfNumbers):
        return False
    return True


if __name__ == '__main__':
    pass
