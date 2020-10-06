import random


def selection_sort(xs):
    for i in range(len(xs)):
        min = i

        for j in range(i + 1, len(xs)):
            if xs[min] > xs[j]:
                min = j

        xs[i], xs[min] = xs[min], xs[i]
    return xs


def quick_sort(xs):
    def split(xs, low, high):
        i = (low - 1)
        pivot = xs[high]
        for j in range(low, high):
            if xs[j] < pivot:
                i += 1
                xs[i], xs[j] = xs[j], xs[i]

        xs[i + 1], xs[high] = xs[high], xs[i + 1]
        return i + 1

    def quick_sort_fun(xs, low, high):
        if low < high:
            split_index = split(xs, low, high)
            if split_index - low < high - split_index:
                quick_sort_fun(xs, low, split_index - 1)
                quick_sort_fun(xs, split_index + 1, high)
            else:
                quick_sort_fun(xs, split_index + 1, high)
                quick_sort_fun(xs, low, split_index - 1)

    quick_sort_fun(xs, 0, len(xs) - 1)
    return xs


def main():
    test_array = [random.random() * 100 - 50 for _ in range(10)]
    print(test_array)
    print(selection_sort(test_array))

    test_array = [random.random() * 100 - 50 for _ in range(10)]
    print(test_array)
    print(quick_sort(test_array))


main()
