import unittest
from mergesort import merge_sort
from bubblesort import bubble_sort

test_case_1 = [3, 12, -3, 0, 324, 11, 2, 7, 2, 9]
test_case_2 = []
test_case_3 = [0]
test_case_4 = [1, -1, 1]
test_case_5 = [1.1, 1, -1.1, -1]
test_case_6 = [1000]
test_case_7 = [0, 0, 0]

test_res_1 = [-3, 0, 2, 2, 3, 7, 9, 11, 12, 324]
test_res_2 = []
test_res_3 = [0]
test_res_4 = [-1, 1, 1]
test_res_5 = [-1.1, -1, 1, 1.1]
test_res_6 = [1000]
test_res_7 = [0, 0, 0]


class TestSortingMethods(unittest.TestCase):

    def test_merge_sort(self):
        self.assertEqual(merge_sort(test_case_1), test_res_1)
        self.assertEqual(merge_sort(test_case_2), test_res_2)
        self.assertEqual(merge_sort(test_case_3), test_res_3)
        self.assertEqual(merge_sort(test_case_4), test_res_4)
        self.assertEqual(merge_sort(test_case_5), test_res_5)
        self.assertEqual(merge_sort(test_case_6), test_res_6)
        self.assertEqual(merge_sort(test_case_7), test_res_7)

    def test_bubble_sort(self):
        self.assertEqual(bubble_sort(test_case_1), test_res_1)
        self.assertEqual(bubble_sort(test_case_2), test_res_2)
        self.assertEqual(bubble_sort(test_case_3), test_res_3)
        self.assertEqual(bubble_sort(test_case_4), test_res_4)
        self.assertEqual(bubble_sort(test_case_5), test_res_5)
        self.assertEqual(bubble_sort(test_case_6), test_res_6)
        self.assertEqual(bubble_sort(test_case_7), test_res_7)


if __name__ == '__main__':
    unittest.main()
