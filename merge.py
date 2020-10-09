def merge(left_list, right_list):
    if len(left_list) == 0:
        return right_list

    if len(right_list) == 0:
        return left_list

    result = []
    left_index = 0
    right_index = 0

    while len(result) < len(left_list) + len(right_list):
        if left_index < len(left_list) and right_index < len(right_list):
            if left_list[left_index] <= right_list[right_index]:
                result.append(left_list[left_index])
                left_index += 1
            else:
                result.append(right_list[right_index])
                right_index += 1

        elif left_index == len(left_list):
            result.append(right_list[right_index])
            right_index += 1
        elif right_index == len(right_list):
            result.append(left_list[left_index])
            left_index += 1

    return result


def merge_sort(array):
    if len(array) < 2:
        return array

    midpoint = len(array) // 2

    return merge(left_list=merge_sort(array[:midpoint]),
                 right_list=merge_sort(array[midpoint:]))
