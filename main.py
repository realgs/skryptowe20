from merge_sort import merge_sort
from quick_sort import quick_sort

if __name__ == '__main__':
    test_list = [4, 65, 67, 2334, 6, 6, 3, 7, 1, 6, 215, 5.6, 2.3, 1, 0]

    merge_copy = test_list.copy()
    quicsort_copy = test_list.copy()

    test_list.sort()
    merge_copy = merge_sort(merge_copy)
    quick_sort(quicsort_copy)
    print(test_list)
    print(merge_copy)
    print(quicsort_copy)

    print('Are they all equal? : {}'.format(test_list == merge_copy and test_list == quicsort_copy))
