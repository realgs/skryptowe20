#!/usr/bin/env python3

unsorted = []
n = int(input("Wpisz ilość elementów: "))
print("Wpisz elementy: ")
for i in range(0, n):
    unsorted.append(int(input()))

changed = True
while changed:
    changed = False
    for i in range(1, n):
        if unsorted[i] < unsorted[i - 1]:
            unsorted[i], unsorted[i - 1] = unsorted[i - 1], unsorted[i]
            changed = True

print(unsorted)
