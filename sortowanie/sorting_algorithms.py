def bubble_sort(list_to_sort):
    for x in range(len(list_to_sort)):
        for y in range(len(list_to_sort) - 1):
            if list_to_sort[y] > list_to_sort[y + 1]:
                list_to_sort[y], list_to_sort[y + 1] = list_to_sort[y + 1], list_to_sort[y]


list1 = [6, 4, 3, 5, 2, 5, 2, 6, 33, 32, 9]
bubble_sort(list1)
print(list1)

list2 = [33, 23, 11, 55, 1, 0, 5, 555, 22]
