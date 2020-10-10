import random
from BubbleSort import bubbleSort
from InsertSort import insertSort

testTable = [random.randint(-1000, 1000) for i in range(20)]
print("Bubble sort - before:")
print(testTable)
bubbleSort(testTable)
print("Bubble sort - after:")
print(testTable)

testTable = [random.randint(-1000, 1000) for i in range(20)]
print("Insert sort - before:")
print(testTable)
insertSort(testTable)
print("Insert sort - after:")
print(testTable)
