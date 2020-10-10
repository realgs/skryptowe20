#alg 1
def bubbleSort(arr):
    n = len(arr)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr
#alg 2
def insertionSort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr
#testing
arr1 = []
arr2 = [1]
arr3 = [5,2]
arr4 = [9,8,7,6,5,4,3,2,1,0]
arr5 = [1,2,3,4,5,6,7,8,9,10]
arr6 = [1,9,2,8,3,7,4,6,5]
arr7 = [1,100,10,100000,1000,10000,10000000,1000000]

print("bubble")
print("presort")
print(arr1)
print(arr2)
print(arr3)
print("postsort")
print(bubbleSort(arr1))
print(bubbleSort(arr2))
print(bubbleSort(arr3))
print("insert")
print("presort")
print(arr4)
print(arr5)
print(arr6)
print(arr7)
print("postsort")
print(insertionSort(arr4))
print(insertionSort(arr5))
print(insertionSort(arr6))
print(insertionSort(arr7))
