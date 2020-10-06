def mergesort(array):
    if len(array) < 2:
        return array

    middle = len(array) // 2
    left = array[:middle]
    right = array[middle:]
    left_idx = right_idx = array_idx = 0
    left_len = len(left)
    right_len = len(right)

    mergesort(left)
    mergesort(right)

    while left_idx < left_len and right_idx < right_len:
        if left[left_idx] <= right[right_idx]:
            array[array_idx] = left[left_idx]
            left_idx += 1
        else:
            array[array_idx] = right[right_idx]
            right_idx += 1
        array_idx += 1

    while left_idx < left_len:
        array[array_idx] = left[left_idx]
        array_idx += 1
        left_idx += 1

    while right_idx < right_len:
        array[array_idx] = right[right_idx]
        array_idx += 1
        right_idx += 1


def __partition_and_sort(array, begin, end):
    if begin >= end - 1:
        return

    pivot = begin
    pivot_value = array[pivot]
    left = begin + 1
    right = end - 1

    while left <= right:
        while left <= right and array[left] <= pivot_value:
            left += 1
        while array[right] > pivot_value:
            right -= 1
        if left < right:
            array[left], array[right] = array[right], array[left]

    array[pivot], array[right] = array[right], array[pivot]
    __partition_and_sort(array, begin, right)
    __partition_and_sort(array, right + 1, end)


def quicksort(array):
    __partition_and_sort(array, 0, len(array))


if __name__ == "__main__":
    import random

    nums = [random.randrange(0, 10) for _ in range(10)]
    print(f"Before: \t{nums}")

    to_mergesort = nums.copy()
    mergesort(to_mergesort)
    print(f"Mergesort: \t{to_mergesort}")

    to_quicksort = nums.copy()
    quicksort(to_quicksort)
    print(f"Quicksort: \t{to_quicksort}")
