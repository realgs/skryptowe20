#!/usr/bin/env python3


def mergesort(lst):
    if len(lst) <= 1:
        return lst
    middle = len(lst) // 2
    left = lst[:middle]
    right = lst[middle:]
    left = mergesort(left)
    right = mergesort(right)
    merged = []
    while len(left) > 0 and len(right) > 0:
        if left[0] < right[0]:
            merged.append(left[0])
            left.pop(0)
        else:
            merged.append(right[0])
            right.pop(0)
    for elem in left:
        merged.append(elem)
    for elem in right:
        merged.append(elem)
    return merged


if __name__ == '__main__':
    unsorted = [9, 21, -2, 0, -2, 22, 31, 13, 8, -71]
    print(mergesort(unsorted))

    unsorted = [9.1, 2119182, -23.092, 0, 3562.87, 0, 938294732894.381, -423.34, 1, -43.1]
    print(mergesort(unsorted))
