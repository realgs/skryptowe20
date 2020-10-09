import unittest
from mergesort import merge_sort
from bubblesort import bubble_sort

test_case_1 = [3, 12, -3, 0, 324, 11, 2, 7, 2, 9]
test_case_2 = []
test_case_3 = [0]
test_case_4 = [1, -1, 1]
test_case_5 = [1.1, 1]
test_case_6 = [1000]
test_case_7 = [0, 0, 0]


class TestSortingMethods(unittest.TestCase):

    def test_merge_sort(self):
        self.assertEqual(merge_sort(test_case_1), [-3, 0, 2, 2, 3, 7, 9, 11, 12, 324])
        self.assertEqual(merge_sort(test_case_2), [])
        self.assertEqual(merge_sort(test_case_3), [0])
        self.assertEqual(merge_sort(test_case_4), [-1, 1, 1])
        self.assertEqual(merge_sort(test_case_5), [1, 1.1])
        self.assertEqual(merge_sort(test_case_6), [1000])
        self.assertEqual(merge_sort(test_case_7), [0, 0, 0])

    def test_bubble_sort(self):
        self.assertEqual(bubble_sort(test_case_1), [-3, 0, 2, 2, 3, 7, 9, 11, 12, 324])
        self.assertEqual(bubble_sort(test_case_2), [])
        self.assertEqual(bubble_sort(test_case_3), [0])
        self.assertEqual(bubble_sort(test_case_4), [-1, 1, 1])
        self.assertEqual(bubble_sort(test_case_5), [1, 1.1])
        self.assertEqual(bubble_sort(test_case_6), [1000])
        self.assertEqual(bubble_sort(test_case_7), [0, 0, 0])


if __name__ == '__main__':
    unittest.main()
