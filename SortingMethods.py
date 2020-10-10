def merge_sort(list):
    pass
def quick_sort(list):
    pass

def do_tests(test_lists):
    sort_algorithms = {'MergeSort': merge_sort, 'QuickSort': quick_sort}
    for name, sort_algorithm in sort_algorithms.items():
        for nr, test_list in enumerate(test_lists):
            test_list_copy = test_list.copy()
            sort_algorithm(test_list_copy)
            print(f'Test listy nr {nr}, algorytmem {name}: ', test_list_copy)

if __name__ == '__main__':
    print(':)')
    test_lists = [[9,8,7,6,5,4,3,2,1], [4,7,1,2,8,6,3,9,5], [1,2,3,6,5,4,7,9,8]]
    do_tests(test_lists)

