def main():
    print("Kacper Szkodzinski - sortowanie liczb.")
    list_to_sort = list([2, 3, 4, 5, 1, 2, 454, 123425, 23, 123, 543, 67, 43, 54, 9213])
    print(list_to_sort)
    print(bubble_sort(list_to_sort))
    print(merge_sort(list_to_sort))


def bubble_sort(init_list):
    copy = list(init_list)
    for i in range(len(copy)):
        for j in range(len(copy)):
            if copy[i] < copy[j]:
                save = copy[j]
                copy[j] = copy[i]
                copy[i] = save
    return copy


def merge_sort(init_list):

    def join(sublist_1, sublist_2):
        if len(sublist_1) == 0:
            return sublist_2
        if len(sublist_2) == 0:
            return sublist_1
        sorted_list = list()
        i = 0
        j = 0
        while not i == len(sublist_1) or not j == len(sublist_2):
            if i == len(sublist_1):
                for k in range(j, len(sublist_2)):
                    sorted_list.append(sublist_2[k])
                    j += 1
            elif j == len(sublist_2):
                for k in range(i, len(sublist_1)):
                    sorted_list.append(sublist_1[k])
                    i += 1
            elif sublist_1[i] < sublist_2[j]:
                sorted_list.append(sublist_1[i])
                i += 1
            else:
                sorted_list.append(sublist_2[j])
                j += 1
        return sorted_list

    def flip(list_of_lists):
        for i in range(len(list_of_lists)):
            if len(list_of_lists[i]) == 2:
                if list_of_lists[i][0] > list_of_lists[i][1]:
                    save = list_of_lists[i][1]
                    list_of_lists[i][1] = list_of_lists[i][0]
                    list_of_lists[i][0] = save

    copy = list(init_list)
    list_of_lists = list([copy])

    while not len(list_of_lists[0]) <= 2:
        new_list_of_lists = list()
        for i in range(len(list_of_lists)):
            new_list_of_lists.append(list_of_lists[i][:len(list_of_lists[i])//2])
            new_list_of_lists.append(list_of_lists[i][len(list_of_lists[i])//2:])
        list_of_lists = new_list_of_lists

    flip(list_of_lists)

    while not len(list_of_lists) == 1:
        new_list_of_lists = list()
        for i in range(0, len(list_of_lists), 2):
            new_list_of_lists.append(join(list_of_lists[i], list_of_lists[i+1]))
        list_of_lists = new_list_of_lists

    return list_of_lists[0]


main()
