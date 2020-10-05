from sorting_methods import mergesort_func, mergesort

if __name__ == '__main__':
    test_case_1 = [1.6, 6.5, 1.5, 1.55, 1.51, -6, 3, 5, 21]
    test_case_2 = [1021, 6, 5, 5, 0, 0, 3]

    print(mergesort_func(test_case_1))
    print(mergesort_func(test_case_2))

    mergesort(test_case_1)
    mergesort(test_case_2)

    print(test_case_1)
    print(test_case_2)