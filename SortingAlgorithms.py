def pancakeSort(array, n):
    current_size = n
    while current_size > 1:
        maxIndex = findMax(array, current_size)
        if maxIndex != current_size - 1:
            flip(array, maxIndex)
            flip(array, current_size - 1)
        current_size -= 1


def bubbleSort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]


def flip(array, i):
    start = 0
    while start < i:
        temp = array[start]
        array[start] = array[i]
        array[i] = temp
        start += 1
        i -= 1


def findMax(array, n):
    maxIndex = 0
    for i in range(0, n):
        if array[i] > array[maxIndex]:
            maxIndex = i
    return maxIndex


def printArray(array, n):
    for i in range(0, n-1):
        print(array[i], end=', ')
    print(array[n-1])


array1 = [13, 0, -10, 10, 13, 15, 20, 4]
array2 = [9, 2, 0, -1, -5, 9, 10, 12]

n1 = len(array1)
n2 = len(array2)
print("Array1 before sorting")
printArray(array1, n1)
print("Array1 after pancake sort")
pancakeSort(array1, n1)
printArray(array1, n1)

print("\nArray2 before sorting")
printArray(array2, n2)
print("Array2 after bubble sort")
bubbleSort(array2)
printArray(array2, n2)
