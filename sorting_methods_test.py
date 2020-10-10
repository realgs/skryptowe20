import unittest

from merge_sort import merge_sort
from quick_sort import quick_sort


class SortingMethodsTest(unittest.TestCase):

    def setUp(self):
        self.positive_integers = [5, 2, 9, 1, 3, 1, 28, 9, 13, 4, 99, 2]
        self.integers = [6, -23, 22, 100, 0, 12, 8, 33, -7, 0, 9, -1, 2, 4, 21]
        self.sorted = [-9, -2, 0, 2, 4, 5, 7, 10]
        self.reversed = [9, 8, 5, 4, 1, 0, -1, -8, -10]
        self.empty = []
        self.one_element = [1]
        self.negative_integers = [-8, -1, -22, -3, -5, -3, -19, -6]
        self.real_numbers = [10.01, 0, 7, -9, 3.4, -0.999, 3, 3.6, 123.32, 21, 6.4, 0.0, 0.1, -0.1]

        self.array_of_arrays = [self.positive_integers, self.integers, self.sorted, self.reversed, self.empty,
                                self.one_element, self.negative_integers, self.real_numbers]

    def test_merge_sort(self):
        for array in self.array_of_arrays:
            self.__sort_equality(array, merge_sort)

    def test_quick_sort(self):
        for array in self.array_of_arrays:
            self.__sort_equality(array, quick_sort)

    def __sort_equality(self, array, sorting_algorithm):
        array_copy = array.copy()
        array_copy.sort()
        sorting_algorithm(array)
        self.assertEqual(array, array_copy)


if __name__ == '__main__':
    unittest.main()
