def merge(list, start_1, end_1, end_2):
    start_2 = end_1 + 1

    if list[end_1] <= list[start_2]:
        return

    while start_1 <= end_1 and start_2 <= end_2:
        if list[start_1] <= list[start_2]:
            start_1 += 1
        else:
            val = list[start_2]
            index = start_2

            while index != start_1:
                list[index] = list[index-1]
                index -= 1

            list[start_1] = val

            start_1 += 1
            end_1 += 1
            start_2 += 1

def merge_sort_reccurence(list, left, right):
    if left < right:
        mid = (left + right) // 2

        merge_sort_reccurence(list, left, mid)
        merge_sort_reccurence(list, mid + 1, right)
        merge(list, left, mid, right)

def merge_sort(list):
    merge_sort_reccurence(list, 0, len(list)-1)

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

