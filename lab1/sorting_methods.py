
def insertion_sort(list):

    for i in  range(1, len(list)):
        current_val = list[i]

        while current_val < list[i - 1] and i > 0:
            list[i] = list[i - 1]
            i -= 1

        list[i] = current_val

def quick_sort(list, min_i, max_i):

    def partition(list, left_i, right_i):

        i = left_i - 1
        pivot = list[right_i]

        for j in range(left_i, right_i):
            if list[j] <= pivot:
                i += 1
                list[i], list[j] = list[j], list[i]

        list[i+1], list[right_i] = list[right_i], list[i+1]
        return i+1

    if min_i < max_i:
        pivot = partition(list, min_i, max_i)
        quick_sort(list, min_i, pivot - 1)
        quick_sort(list, pivot + 1, max_i)

