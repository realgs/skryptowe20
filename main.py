from sorting_methods import quicksort
from sorting_methods import bubble_sort


def sort_testing(list_of_unsorted_list):
    for unsorted_list in list_of_unsorted_list:
        quicksort_list = unsorted_list[:]
        bubble_sort_list = unsorted_list[:]
        python_sort_list = unsorted_list[:]
        quicksort_result = quicksort(quicksort_list)
        bubble_sort_result = bubble_sort(bubble_sort_list)
        python_sort_list.sort()

        print("New test:")
        print(" Unsorted list: " + str(unsorted_list))
        print(" Result of quicksort: " + str(quicksort_result) + " - is good sorted?: " + str(quicksort_result == python_sort_list))
        print(" Result of bubble_sort: " + str(bubble_sort_result) + " - is good sorted?: " + str(bubble_sort_result == python_sort_list))


def run_test():
    list1 = [1, 7, 4, 3, 5, 7, 4, -3, 57, -4, 3, 5, 3, 3, 5, 0, 3, 5, 64, 654, 3645, 432356, 4645, 234]
    list2 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    list3 = ["aa", "aaaa", "a", "z", "sda", "zz", "sasa", "zzzz", "swe", "zzz"]
    list4 = []
    list_of_list = [list1, list2, list3, list4]
    sort_testing(list_of_list)


if __name__ == '__main__':
    run_test()
