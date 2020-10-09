#quicksort algorithm
def myQuickSort(arr):
    number_of_elements = len(arr)
    pivot = 0
    # array with 1 element
    if len(arr) < 2:
        return arr

    current_position = pivot
    # partition
    for i in range(1, number_of_elements):
        if arr[i] <= arr[pivot]:
            current_position += 1
            temp = arr[i]
            arr[i] = arr[current_position]
            arr[current_position] = temp

    temp = arr[0]
    arr[0] = arr[current_position]
    arr[current_position] = temp

    left = myQuickSort(arr[0:current_position])
    right = myQuickSort(arr[current_position + 1:number_of_elements])

    arr = left + [arr[current_position]] + right

    return arr


array_to_sort = [-3, 11, 0, 4,  1000, 4, 0, -1, -1, -1, 23, 11]
sorted_array_asc = [-3, -1, -1, -1, 0, 0, 4, 4, 11, 11, 23, 1000]
sorted_array_desc = [1000, 23, 11, 11, 4, 4, 0, 0, -1, -1, -1, -3]
print("Quicksort: ")
print("Test 1 with random array: ", myQuickSort(array_to_sort))
print("Test 2 with sorted asc array: ", myQuickSort(sorted_array_asc))
print("Test 3 with sorted desc array: ", myQuickSort(sorted_array_desc))