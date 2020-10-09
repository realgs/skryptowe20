def bubble_sort(list_to_sort):
    for x in range(len(list_to_sort)):
        for y in range(len(list_to_sort) - 1):
            if list_to_sort[y] > list_to_sort[y + 1]:
                list_to_sort[y], list_to_sort[y + 1] = list_to_sort[y + 1], list_to_sort[y]


def merge_sort(list_to_sort):
    if len(list_to_sort) > 1:
        m = len(list_to_sort) // 2
        left = list_to_sort[:m]
        right = list_to_sort[m:]
        left = merge_sort(left)
        right = merge_sort(right)

        list_to_sort = []

        while len(left) > 0 and len(right) > 0:
            if left[0] < right[0]:
                list_to_sort.append(left[0])
                left.pop(0)
            else:
                list_to_sort.append(right[0])
                right.pop(0)

        for i in left:
            list_to_sort.append(i)
        for i in right:
            list_to_sort.append(i)

    return list_to_sort


list1 = [6, 4, 3, 5, 2, 5, 2, 6, 33, 32, 9]
bubble_sort(list1)
print(list1)

list2 = [33, 23, 11, 55, 1, 0, 5, 555, 22, 11]
print(merge_sort(list2))
