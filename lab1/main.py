from sorting_methods import insertion_sort, quick_sort

def main():
    list_to_insertion_sort = [9, 13, 0, 2, 34, 17, 5]
    list_to_quick_sort = [34, 2, 8, 15, 20, 7, 0]

    print("Insertion sort")
    print(list_to_insertion_sort)
    insertion_sort(list_to_insertion_sort)
    print(list_to_insertion_sort)

    print("\nQuick sort")
    print(list_to_quick_sort)
    quick_sort(list_to_quick_sort, 0, len(list_to_quick_sort)-1)
    print(list_to_quick_sort)

if __name__ == "__main__":
    main()