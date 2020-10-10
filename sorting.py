def bubble_sort(array):
    length = len(array)
    for i in range(length - 1):
        for j in range(length - i - 1):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]


def quick_sort(array, low, high):
    if high > low:
        p = partition(array, low, high)
        quick_sort(array, low, p - 1)
        quick_sort(array, p + 1, high)


def partition(array, low, high):
    divider = low
    pivot = high

    for i in range(low, high):
        if array[i] < array[pivot]:
            array[i], array[divider] = array[divider], array[i]
            divider += 1

    array[pivot], array[divider] = array[divider], array[pivot]

    return divider


if __name__ == '__main__':
    first_array = [5, 0, 8, 1.23, 93, 21, 54, 87, 13.10]
    second_array = [-4, 10, -2.4, -3, 5, 11.02, -14, 7]
    print(first_array)
    bubble_sort(first_array)
    print("sorted:", first_array)
    print(second_array)
    quick_sort(second_array, 0, len(second_array)-1)
    print("sorted:", second_array)
