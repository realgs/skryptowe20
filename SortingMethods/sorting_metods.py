from random import randint


class SortingMethods():
    def __insertion_sort(self, list_to_sort, low, high):
        if len(list_to_sort) <= 0:
            return
        for i in range(low + 1, high):
            elem_to_insert = list_to_sort[i]
            j = i - 1
            while j >= 0 and list_to_sort[j] > elem_to_insert:
                list_to_sort[j + 1] = list_to_sort[j]
                j -= 1
            list_to_sort[j + 1] = elem_to_insert

    def __partition(self, li_sort, low, high):
        piv_pos = randint(low, high)  # picking random element as pivot
        pivot = li_sort[piv_pos]
        li_sort[piv_pos], li_sort[high] = li_sort[high], li_sort[piv_pos]
        i = (low - 1)
        for j in range(low, high):
            if li_sort[j] < pivot:
                i += 1
                li_sort[i], li_sort[j] = li_sort[j], li_sort[i]
        li_sort[i + 1], li_sort[high] = li_sort[high], li_sort[i + 1]
        return i + 1

    def quick_sort(self, list_to_sort, low, high):
        if low < high:
            pi = self.__partition(list_to_sort, low, high)
            if high - low < 10:
                self.__insertion_sort(list_to_sort, low, high + 1)
                low = high
            else:
                self.quick_sort(list_to_sort, low, pi - 1)
                self.quick_sort(list_to_sort, pi + 1, high)

    def merge_sort(self, arr):
        if len(arr) > 1:
            middle = len(arr) // 2
            left_arr = self.merge_sort(arr[:middle])
            right_arr = self.merge_sort(arr[middle:])

            arr = []
            while len(left_arr) > 0 and len(right_arr) > 0:
                if left_arr[0] < right_arr[0]:
                    arr.append(left_arr[0])
                    left_arr.pop(0)
                else:
                    arr.append(right_arr[0])
                    right_arr.pop(0)

            for val in left_arr:
                arr.append(val)
            for val in right_arr:
                arr.append(val)
        return arr