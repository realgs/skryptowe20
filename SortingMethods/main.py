import sorting_metods as sm
from random import shuffle

sorts = sm.SortingMethods()

base_test_list = list(range(-100, 100))
shuffle(base_test_list)

test_list = base_test_list.copy()
print(base_test_list)
print(test_list)
sorts.quick_sort(test_list, 0, len(test_list)-1)
print("quick sorting")
print(test_list)



