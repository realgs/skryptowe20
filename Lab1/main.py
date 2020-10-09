from sorting_methods import bubble_sort, merge_sort
from random import randint

def test_sorting_method(sorting_method, arrays_dictionary):
    for name, array in arrays_dictionary.items():
        print(f"test {name}\n\tinput:{array}\n\tsolution:{sorting_method(array)}")

def main():
    arrays_dictionary = {
        "emptyArray" : [],
        "simpleArray" : [5, 1, 2, 3, 4],
        "sortedArray" : [1, 2, 4, 6, 9, 123],
        "negativeArray" : [-123, -534, -1239, -9, -43],
        "randomArray" : [randint(-100, 100) for _ in range(0, 10)]
    }

    test_sorting_method(bubble_sort, arrays_dictionary)
    test_sorting_method(merge_sort, arrays_dictionary)

if __name__ == "__main__":
    main()