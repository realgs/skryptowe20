import unittest
from sortingAlgorithms import bubble_sort
from sortingAlgorithms import shell_sort


class TestSortingAlgorithms(unittest.TestCase):
    def setUp(self):
        self.numbers_correct_output = [-3, -1, 0, 5, 7, 9, 10]
        self.strings_correct_output = ["cat", "dog", "home", "house", "python", "snake", "zoo"]

    def test_sorting_methods(self):
        self.test_algorithm(bubble_sort, self.__get_input_number_lists(), self.numbers_correct_output)
        self.test_algorithm(shell_sort, self.__get_input_string_lists(), self.strings_correct_output)

    def test_algorithm(self, sorting_algorithm, input_lists, correct_output_list):
        for i in range(0, len(input_lists)):
            sorting_algorithm(input_lists[i])
            self.assertListEqual(input_lists[i], correct_output_list)

    @staticmethod
    def __get_input_number_lists():
        number_input_lists = [[-3, -1, 0, 5, 7, 9, 10],
                              [10, 9, 7, 5, 0, -1, -3],
                              [-3, 5, 0, 9, 7, -1, 10],
                              [0, 5, 7, 9, 10, -3, -1]]
        return number_input_lists

    @staticmethod
    def __get_input_string_lists():
        string_input_lists = [["cat", "dog", "home", "house", "python", "snake", "zoo"],
                              ["zoo", "snake", "python", "house", "home", "dog", "cat"],
                              ["cat", "house", "home", "snake", "python", "dog", "zoo"],
                              ["home", "house", "python", "snake", "zoo", "cat", "dog"]]
        return string_input_lists
