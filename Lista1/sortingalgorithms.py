def bubble_sort(array):
    iteration_count = len(array) - 1
    while iteration_count > 0:
        swaps = 0
        for index in range(iteration_count):
            if array[index] > array[index + 1]:
                array[index], array[index+1] = array[index+1], array[index]
                swaps += 1
        if swaps == 0:
            return
        else:
            iteration_count -= 1


def quick_sort(array):
    def helper(left, right):
        if left < right:
            pivot = divide_array(left, right)
            helper(left, pivot-1)
            helper(pivot+1, right)

    def divide_array(left, right):
        pivot_index = left + (right - left) // 2
        pivot_value = array[pivot_index]
        array[pivot_index], array[right] = array[right], array[pivot_index]
        current_position = left
        for index in range(left, right):
            if array[index] < pivot_value:
                array[index], array[current_position] = array[current_position], array[index]
                current_position += 1
        array[current_position], array[right] = array[right], array[current_position]
        return current_position

    helper(0, len(array)-1)


if __name__ == "__main__":
    test_array_1 = [5, 2, 6, 1, 9, 3, 8, 7, 4]
    print("Test array:", test_array_1)
    bubble_sort(test_array_1)
    print("Test array after bubble sort:", test_array_1, "\n")

    test_array_2 = [5, 2, 6, 1, 9, 3, 8, 7, 4]
    print("Test array:", test_array_2)
    bubble_sort(test_array_2)
    print("Test array after quick sort:", test_array_2, "\n")
