def merge_sorted(lst: list) -> list:
    def merge(a_lst: list, b_lst: list) -> list:
            merged = []
            a_index = 0
            b_index = 0
            while not len(merged) == len(a_lst) + len(b_lst):
                if a_index == len(a_lst):
                    merged += b_lst[b_index:]
                    break
                if b_index == len(b_lst):
                    merged += a_lst[a_index:]
                    break
                if a_lst[a_index] < b_lst[b_index]:
                    merged.append(a_lst[a_index])
                    a_index += 1
                else:
                    merged.append(b_lst[b_index])
                    b_index += 1
            return merged

    def split(lst: list) -> tuple:
            return lst[:len(lst) // 2], lst[len(lst) // 2:]

    def subsort(lst: list) -> list:
        if len(lst) <= 1:
            return lst
        a, b = split(lst)
        return merge(subsort(a), subsort(b))

    return subsort(lst)

def cocktail_sorted(lst: list) -> list:
    lst = lst[:]
    if len(lst) <= 1:
        return lst
    bottom, top = 0, len(lst) - 1
    swapped = True
    while swapped:
        swapped = False
        for i in range(bottom, top):
            if lst[i] > lst[i+1]:
                lst[i], lst[i+1] = lst[i+1], lst[i]
                swapped = True
        top -= 1
        for i in range(top, bottom, -1):
            if lst[i] < lst[i-1]:
                lst[i], lst[i-1] = lst[i-1], lst[i]
                swapped = True
        bottom += 1
    return lst