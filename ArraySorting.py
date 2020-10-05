from enum import Enum

class SortAlgorithm(Enum):
    QuickSort = 1
    InsertSort = 2

def Sort(arr:[], alg: SortAlgorithm) -> []:
    if alg is SortAlgorithm.QuickSort:
        return QuickSort(arr)
    elif alg is SortAlgorithm.QuickSort:
        return InsertSort(arr)


def QuickSort(arr1: []) -> []:
    pass

def InsertSort(arr1: []) -> []:
    pass