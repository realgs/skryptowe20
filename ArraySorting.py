from enum import Enum

class SortAlgorithm(Enum):
    QuickSort = 1
    InsertSort = 2

def Sort(arr:[], alg: SortAlgorithm):
    if alg is SortAlgorithm.QuickSort:
        return QuickSort(arr)
    elif alg is SortAlgorithm.InsertSort:
        return InsertSort(arr)


def QuickSort(arr: []):
    def partition(arr, low, high):
        i = (low - 1)
        pivot = arr[high]

        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]

        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return (i + 1)

    def InternalQuickSort(arr:[], low: int, high: int):
        if len(arr) == 1:
            return
        if low < high:
            part = partition(arr, low, high)

            InternalQuickSort(arr, low, part - 1)
            InternalQuickSort(arr, part + 1, high)

    InternalQuickSort(arr, 0, len(arr) - 1)



def InsertSort(arr: []):
    pass