from sorting_methods import mergesort, bubblesort

if __name__ == "__main__":
  list = [4, 3, 5, 7, 43, 2, 5, 6, 87, 4, 3, 1, 3, 4, 5, 6, 7, 45, 3, 2]

  sorted1 = mergesort(list)
  sorted2 = bubblesort(list)

  print(sorted1)
  print(sorted2)
  print(sorted1 == sorted2)
