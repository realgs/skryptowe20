def merge_sort(list_to_sort):
    def _merge(start_1, end_1, end_2):
        start_2 = end_1 + 1

        if list_to_sort[end_1] <= list_to_sort[start_2]:
            return

        while start_1 <= end_1 and start_2 <= end_2:
            if list_to_sort[start_1] <= list_to_sort[start_2]:
                start_1 += 1
            else:
                val = list_to_sort[start_2]
                index = start_2

                while index != start_1:
                    list_to_sort[index] = list_to_sort[index - 1]
                    index -= 1

                list_to_sort[start_1] = val

                start_1 += 1
                end_1 += 1
                start_2 += 1

    def _merge_sort(left, right):
        if left < right:
            mid = (left + right) // 2

            _merge_sort(left, mid)
            _merge_sort(mid + 1, right)
            _merge(left, mid, right)

    _merge_sort(0, len(list_to_sort)-1)

def quick_sort(list_to_sort):
    def _partition(left, right):
        i = left - 1
        pivot = list_to_sort[right]

        for j in range(left, right):
            if list_to_sort[j] <= pivot:
                i = i + 1
                list_to_sort[i], list_to_sort[j] = list_to_sort[j], list_to_sort[i]

        list_to_sort[i+1], list_to_sort[right] = list_to_sort[right], list_to_sort[i+1]
        return i+1

    def _quick_sort(left, right):
        if len(list_to_sort) == 1:
            return list_to_sort
        if left < right:
            pi = _partition(left, right)
            _quick_sort(left, pi-1)
            _quick_sort(pi+1, right)

    _quick_sort(0, len(list_to_sort)-1)

def do_tests(test_lists):
    sort_algorithms = {'MergeSort': merge_sort, 'QuickSort': quick_sort}
    for name, sort_algorithm in sort_algorithms.items():
        for nr, test_list in enumerate(test_lists):
            test_list_copy = test_list.copy()
            sort_algorithm(test_list_copy)
            print(f'Test listy nr {nr}, algorytmem {name}: ', test_list_copy)

if __name__ == '__main__':
    test_lists = [[9,8,7,6,5,4,3,2,1], [4,7,1,2,8,6,3,9,5], [1,2,3,6,5,4,7,9,8]]
    do_tests(test_lists)

