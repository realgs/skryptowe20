from random import shuffle

def swap(array, a, b):
    array[a], array[b] = array[b], array[a]

def bubble_sort(array):
    length = len(array);
    for i in range(length):
        for j in range(length - i - 1):
            if array[j] > array[j+1]:
                 swap(array, j, j+1)

def quick_sort(array):
    def quick_sort_helper(left, right):
        if left >= right:
            return
        p = partition(left, right)
        quick_sort_helper(left, p-1)
        quick_sort_helper(p+1, right)

    def partition(left, right):
        pivot = array[right]
        i = left
        for j in range(left, right):
            if array[j] <= pivot:
                swap(array, i, j)
                i = i + 1
        swap(array, i, right)
        return i

    quick_sort_helper(0, len(array)-1)

def test_sorting_method(sorted_array, array, method):
    method(array)
    return array == sorted_array

def test_sorting_methods(array, methods):
    sorted_array = array
    sorted_array.sort()
    for method in methods:
        if not test_sorting_method(sorted_array, array[:], method):
            return False
    return True

def print_test_outcome(test_outcome):
    if test_outcome:
        print("OK")
    else:
        print("ERROR")

def main():
    methods = [bubble_sort, quick_sort]
    array_of_integers = list(range(20))
    shuffle(array_of_integers)
    print_test_outcome(test_sorting_methods(array_of_integers, methods))
    array_of_chars = ['b', 'u', 'x', 'z', 's', 'a']
    print_test_outcome(test_sorting_methods(array_of_chars, methods))

if __name__ == "__main__":
    main()
