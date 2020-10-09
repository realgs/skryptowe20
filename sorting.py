def bubble_sort_numbers(numbers_to_sort):
    numbers = numbers_to_sort.copy()
    if len(numbers) > 1:
        numbers_len = len(numbers)
        for _ in range(numbers_len):
            was_moved = False
            for i in range(numbers_len - 1):
                if numbers[i] > numbers[i + 1]:
                    numbers[i + 1], numbers[i] = numbers[i], numbers[i + 1]
                    was_moved = True
            if not was_moved:
                break
    return numbers


def quick_sort_numbers(numbers_to_sort):
    def partition(numbers, n_0, n_1):
        last_smaller_index = n_0 - 1
        pivot = numbers[n_1]
        for j in range(n_0, n_1):
            if numbers[j] <= pivot:
                last_smaller_index = last_smaller_index + 1
                numbers[last_smaller_index], numbers[j] = numbers[j], numbers[last_smaller_index]
        numbers[last_smaller_index + 1], numbers[n_1] = numbers[n_1], numbers[last_smaller_index + 1]
        return last_smaller_index + 1

    def quick_sort_internal(numbers, n_0, n_1):
        if n_0 < n_1:
            pivot_index = partition(numbers, n_0, n_1)
            quick_sort_internal(numbers, n_0, pivot_index - 1)
            quick_sort_internal(numbers, pivot_index + 1, n_1)
        return numbers

    return quick_sort_internal(numbers_to_sort.copy(), 0, len(numbers_to_sort) - 1)
