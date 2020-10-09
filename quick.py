def partition(nums_array, low, high):
    pivot = nums_array[(low + high) // 2]
    i = low - 1
    j = high + 1
    while True:
        i += 1
        while nums_array[i] < pivot:
            i += 1

        j -= 1
        while nums_array[j] > pivot:
            j -= 1

        if i >= j:
            return j
        else:
            nums_array[i], nums_array[j] = nums_array[j], nums_array[i]


def quick_sort(nums_array):
    def sort(nums, low, high):
        if low < high:
            split_index = partition(nums, low, high)
            sort(nums, low, split_index)
            sort(nums, split_index + 1, high)

    sort(nums_array, 0, len(nums_array) - 1)
