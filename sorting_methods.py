
def swap(my_list, left, right):
    if left != right:
        temp = my_list[left]
        my_list[left] = my_list[right]
        my_list[right] = temp


def bubble_sort(my_list):
    right_max_index = len(my_list) - 1
    while right_max_index > 0:
        last_checked = 0
        for i in range(right_max_index):
            if my_list[i] > my_list[i+1]:
                swap(my_list, i, i + 1)
                last_checked = i
        right_max_index = last_checked
    return my_list
