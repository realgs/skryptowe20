import sorting_methods

if __name__ == "__main__":
    arr_for_quicksort = [7, 1, 2, 5, 3, 4, 32, 6]
    arr_for_quicksort_desc = [9, 8, 7, 6, 5, 4, 3, 2, 1]
    arr_for_quicksort_same_numbers = [1, 1, 1, 1, 1, 1, 1]
    arr_for_quicksort_negative_numbers = [-3, -71, 32, -999, 32, 8]
    arr_for_quicksort_decimal_numbers = [1.06, -71, 5.124, 0, 32.5]

    sorting_methods.quicksort(arr_for_quicksort)
    sorting_methods.quicksort(arr_for_quicksort_desc)
    sorting_methods.quicksort(arr_for_quicksort_same_numbers)
    sorting_methods.quicksort(arr_for_quicksort_negative_numbers)
    sorting_methods.quicksort(arr_for_quicksort_decimal_numbers)

    print(arr_for_quicksort)
    print(arr_for_quicksort_desc)
    print(arr_for_quicksort_same_numbers)
    print(arr_for_quicksort_negative_numbers)
    print(arr_for_quicksort_decimal_numbers)

    arr_for_heapsort = [7, 1, 2, 5, 3, 4, 32, 6]
    arr_for_heapsort_desc = [9, 8, 7, 6, 5, 4, 3, 2, 1]
    arr_for_heapsort_same_numbers = [1, 1, 1, 1, 1, 1, 1]
    arr_for_heapsort_negative_numbers = [-3, -71, 32, -999, 32, 8]
    arr_for_heapsort_decimal_numbers = [1.06, -71, 5.124, 0, 32.5]

    sorting_methods.heapsort(arr_for_heapsort)
    sorting_methods.heapsort(arr_for_heapsort_desc)
    sorting_methods.heapsort(arr_for_heapsort_same_numbers)
    sorting_methods.heapsort(arr_for_heapsort_negative_numbers)
    sorting_methods.heapsort(arr_for_heapsort_decimal_numbers)

    print(arr_for_heapsort)
    print(arr_for_heapsort_desc)
    print(arr_for_heapsort_same_numbers)
    print(arr_for_heapsort_negative_numbers)
    print(arr_for_heapsort_decimal_numbers)
