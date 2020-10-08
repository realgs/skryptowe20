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
    unsorted = []
    n = int(input("Wpisz ilość elementów: "))
    print("Wpisz elementy: ")
    for i in range(0, n):
        unsorted.append(int(input()))

    print(mergesort(unsorted))
