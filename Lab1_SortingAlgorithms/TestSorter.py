import unittest
from Lab1_SortingAlgorithms import sorter


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.list_int_plus = [5, 7, 9, 4, 1, 2, 3]
        self.list_sorted = [1, 2, 3, 4, 5]
        self.list_reversed = [9, 8, 7, 6, 5, 4, 3, 2, 1]
        self.list_minus = [-7, -6, -4, -7, -1]
        self.list_all = [5, 6, 7, 7.0, 9.1, -7.7, -2.4, 9, .4, 8.6, 7, -19, -4, -3]

    def test_selection_sort(self):
        sorter.sort(self.list_int_plus, "selection")
        sorter.sort(self.list_sorted, "selection")
        sorter.sort(self.list_reversed, "selection")
        sorter.sort(self.list_minus, "selection")
        sorter.sort(self.list_all, "selection")

        self.assertEqual(self.list_int_plus, [1, 2, 3, 4, 5, 7, 9])
        self.assertEqual(self.list_sorted, [1, 2, 3, 4, 5])
        self.assertEqual(self.list_reversed, [1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.assertEqual(self.list_minus, [-7, -7, -6, -4, -1])
        self.assertEqual(self.list_all, [-19, -7.7, -4, -3, -2.4, 0.4, 5, 6, 7, 7, 7.0, 8.6, 9, 9.1])

    def test_quick_sort(self):
        sorter.sort(self.list_int_plus)
        sorter.sort(self.list_sorted)
        sorter.sort(self.list_reversed)
        sorter.sort(self.list_minus)
        sorter.sort(self.list_all)

        self.assertEqual(self.list_int_plus, [1, 2, 3, 4, 5, 7, 9])
        self.assertEqual(self.list_sorted, [1, 2, 3, 4, 5])
        self.assertEqual(self.list_reversed, [1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.assertEqual(self.list_minus, [-7, -7, -6, -4, -1])
        self.assertEqual(self.list_all, [-19, -7.7, -4, -3, -2.4, 0.4, 5, 6, 7, 7, 7.0, 8.6, 9, 9.1])


if __name__ == '__main__':
    unittest.main()
