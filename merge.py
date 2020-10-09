def merge(left_list, right_list):
    if len(left_list) == 0:
        return right_list

    if len(right_list) == 0:
        return left_list

    result = []
    index_left = 0
    index_right = 0

    while len(result) < len(left_list) + len(right_list):
        if index_left < len(left_list) and index_right < len(right_list):
            if left_list[index_left] <= right_list[index_right]:
                result.append(left_list[index_left])
                index_left += 1
            else:
                result.append(right_list[index_right])
                index_right += 1

        elif index_left == len(left_list):
            result.append(right_list[index_right])
            index_right += 1
        elif index_right == len(right_list):
            result.append(left_list[index_left])
            index_left += 1

    return result


def merge_sort(array):
    if len(array) < 2:
        return array

    midpoint = len(array) // 2

    return merge(left_list=merge_sort(array[:midpoint]),
                 right_list=merge_sort(array[midpoint:]))


array = [12, 5, 1, -10, 65, 5, 3, 9, 10, 2, -60, 1432, 13, 7, 5, 2, 34]
array = merge_sort(array)
print(array)