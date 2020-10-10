import sorting_methods

if __name__ == "__main__":
    arr_for_quicksort = [7, 1, 2, 5, 3, 4, 32, 6]
    arr_for_quicksort_desc = [9, 8, 7, 6, 5, 4, 3, 2, 1]
    arr_for_quicksort_same_numbers = [1, 1, 1, 1, 1, 1, 1]

    sorting_methods.quicksort(arr_for_quicksort)
    sorting_methods.quicksort(arr_for_quicksort_desc)
    sorting_methods.quicksort(arr_for_quicksort_same_numbers)

    print(arr_for_quicksort)
    print(arr_for_quicksort_desc)
    print(arr_for_quicksort_same_numbers)
