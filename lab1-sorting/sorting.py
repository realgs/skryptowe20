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


if __name__ == "__main__":
    xs = [3,6,8,9]
    ys = [1,2,5,7]

    print(merge(xs, ys))