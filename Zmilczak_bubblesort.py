#!/usr/bin/env python3

unsorted = [8.08, 2284934710, 228021, -3.831, -8.1, 0, -13, 21.1833124, -13, -1938234.49029]

changed = True
while changed:
    changed = False
    for i in range(1, len(unsorted)):
        if unsorted[i] < unsorted[i - 1]:
            unsorted[i], unsorted[i - 1] = unsorted[i - 1], unsorted[i]
            changed = True

print(unsorted)
