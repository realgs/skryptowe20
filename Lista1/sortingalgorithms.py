def swap(arr, index1, index2):
    temp = arr[index1]
    arr[index1] = arr[index2]
    arr[index2] = temp


def bubble_sort(array):
    iteration_count = len(array) - 1
    while iteration_count > 0:
        swaps = 0
        for index in range(iteration_count):
            if array[index] > array[index + 1]:
                swap(array, index, index+1)
                swaps += 1
        if swaps == 0:
            return
        else:
            iteration_count -= 1


if __name__ == "__main__":
    test_array_1 = [5, 2, 6, 1, 9, 3, 8, 7, 4]
    print("test array:", test_array_1)
    bubble_sort(test_array_1)
    print("Test array after bubble sort:", test_array_1)
