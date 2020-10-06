import math

SHELL_SORT_GAP_SEQUENCES_AMOUNT = 70


def swap(array, left_index, right_index):
    array[left_index], array[right_index] = array[right_index], array[left_index]


def bubble_sort(self, array):
    for passed_elements in range(1, len(array)):
        for left_element_index in range(0, len(array) - passed_elements):
            if array[left_element_index] > array[left_element_index + 1]:
                self.swap(array, left_element_index, left_element_index + 1)


def shell_sort(array):
    gap_sequences = __get_shell_sort_gap_sequences()
    iteration = 1
    distance = gap_sequences[len(gap_sequences) - iteration]

    while distance > 0:
        for i in range(distance, len(array)):
            element = array[i]
            j = i
            while j >= distance and element < array[j - distance]:
                array[j] = array[j - distance]
                j -= distance

            array[j] = element
        iteration += 1
        distance = gap_sequences[len(gap_sequences) - iteration]


def __get_shell_sort_gap_sequences():
    gap_sequences = [0]
    for i in range(0, SHELL_SORT_GAP_SEQUENCES_AMOUNT):
        distance = 1.8 * (2.25 ** i) - 0.8
        gap_sequences.append(math.ceil(distance))

    return gap_sequences
