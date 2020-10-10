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

if __name__ == "__main__":
    xs = [1,7,4,9,0,5,8,3,6,2]
    ys = []

    print(subsort(xs), subsort(ys))