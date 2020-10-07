

def partition(list, first, last):
    pivot = list[first]
    l = first + 1
    out = last
    while True:
        while l <= out and list[out] >= pivot:
            out = out - 1
        while l <= out and list[l] <= pivot:
            l = l + 1

        if l <= out:
            list[l], list[out] = list[out], list[l]
        else:
            break
    list[first], list[out] = list[out], list[first]
    return out


def quickSort(list, first, last):
    if first >= last:
        return
    p = partition(list, first, last)
    quickSort(list, first, p - 1)
    quickSort(list, p + 1, last)


def mergeSort(list, left, right):
    if left >= right:
        return

    p = (left + right) // 2
    mergeSort(list, left, p)
    mergeSort(list, p + 1, right)
    merge(list, left, right, p)


def merge(list, left, right, p):

    leftsameinx = 0
    rightsameinx = 0
    sort = left
    leftsame = list[left:p + 1]
    rightsame = list[p + 1:right + 1]


    while leftsameinx < len(leftsame) and rightsameinx < len(rightsame):

        if leftsame[leftsameinx] <= rightsame[rightsameinx]:
            list[sort] = leftsame[leftsameinx]
            leftsameinx = leftsameinx + 1

        else:
            list[sort] = rightsame[rightsameinx]
            rightsameinx = rightsameinx + 1
        sort = sort + 1

    while leftsameinx < len(leftsame):
        list[sort] = leftsame[leftsameinx]
        leftsameinx = leftsameinx + 1
        sort = sort + 1

    while rightsameinx < len(rightsame):
        list[sort] = rightsame[rightsameinx]
        rightsameinx = rightsameinx + 1
        sort = sort + 1


if __name__ == '__main__':
    test1= [2,0,6,12,15,4,5,28,10,1,9]
    quickSort(test1, 0, len(test1) - 1)

    test2 = [12,54,2,4,7,45,3,54,21,34,45,13,17,8,0,11]
    mergeSort(test2, 0, len(test2) - 1)

    print(test1)
    print(test2)



