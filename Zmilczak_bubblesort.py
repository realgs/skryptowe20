#!/usr/bin/env python3

unsorted = [8, 21, 3, -8, 0, -13, 2, 21, -9]

changed = True
while changed:
    changed = False
    for i in range(1, n):
        if unsorted[i] < unsorted[i - 1]:
            unsorted[i], unsorted[i - 1] = unsorted[i - 1], unsorted[i]
            changed = True

print(unsorted)
