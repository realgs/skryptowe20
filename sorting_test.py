import unittest

from sorting import bubble_sort_numbers, quick_sort_numbers

test_numbers = [
    {
        "source": [4, 3, 2, 1],
        "expected": [1, 2, 3, 4]
    },
    {
        "source": [],
        "expected": []
    },
    {
        "source": [-4, -322, -22, -1, 0, 123, 123, 563],
        "expected": [-322, -22, -4, -1, 0, 123, 123, 563]
    },
    {
        "source": [123, 546546, 234, 4, 1, 2, -213, -2222],
        "expected": [-2222, -213, 1, 2, 4, 123, 234, 546546]
    },
    {
        "source": [8123, 1, 1, 1, 1, 2, 2, -32, -23, -23, 13292],
        "expected": [-32, -23, -23, 1, 1, 1, 1, 2, 2, 8123, 13292]
    },
    {
        "source": [100_000_000, 423, 1244, 654, 1, -42, -1000],
        "expected": [-1000, -42, 1, 423, 654, 1244, 100_000_000]
    }
]


class SortingAlgorithmTest(unittest.TestCase):

    def test_bubble_sort(self):
        for test_data in test_numbers:
            with self.subTest():
                numbers = test_data['source']
                expected_sorted_numbers = test_data['expected']
                sorted_numbers = bubble_sort_numbers(numbers)
                self.assertEqual(expected_sorted_numbers, sorted_numbers)

    def test_quick_sort(self):
        for test_data in test_numbers:
            with self.subTest():
                numbers = test_data['source']
                expected_sorted_numbers = test_data['expected']
                sorted_numbers = quick_sort_numbers(numbers)
                self.assertEqual(expected_sorted_numbers, sorted_numbers)
