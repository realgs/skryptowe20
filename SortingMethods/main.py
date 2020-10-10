import sorting_metods as sm
from random import shuffle
import unittest


class TestSorts(unittest.TestCase):
    int_test_list = list(range(-50, 50))
    nat_test_list = list(range(100))
    real_test_list = [x/10 for x in list(range(100))]
    sorts = sm.SortingMethods()

    def test_quicksort_int(self):
        test_list = self.int_test_list.copy()
        shuffle(test_list)
        self.sorts.quick_sort(test_list, 0, len(test_list)-1)
        self.assertEqual(test_list, self.int_test_list, msg="Lists are not equal")

    def test_quicksort_nat(self):
        test_list = self.nat_test_list.copy()
        shuffle(test_list)
        self.sorts.quick_sort(test_list, 0, len(test_list)-1)
        self.assertEqual(test_list, self.nat_test_list, msg="Lists are not equal")

    def test_quicksort_real(self):
        test_list = self.real_test_list.copy()
        shuffle(test_list)
        self.sorts.quick_sort(test_list, 0, len(test_list)-1)
        self.assertEqual(test_list, self.real_test_list, msg="Lists are not equal")

    def test_mergesort_int(self):
        test_list = self.int_test_list.copy()
        shuffle(test_list)
        test_list = self.sorts.merge_sort(test_list)
        self.assertEqual(test_list, self.int_test_list, msg="Lists are not equal")

    def test_mergesort_nat(self):
        test_list = self.nat_test_list.copy()
        shuffle(test_list)
        test_list = self.sorts.merge_sort(test_list)
        self.assertEqual(test_list, self.nat_test_list, msg="Lists are not equal")

    def test_mergesort_real(self):
        test_list = self.real_test_list.copy()
        shuffle(test_list)
        test_list = self.sorts.merge_sort(test_list)
        self.assertEqual(test_list, self.real_test_list, msg="Lists are not equal")


if __name__ == '__main__':
    unittest.main()