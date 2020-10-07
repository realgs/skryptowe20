import random

def insert_sort(arr):
    for i in range(1, len(arr)):
        value = arr[i]

        j = i-1
        while j>=0 and value < arr[j]:
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = value

def quick_sort(arr):
    __quick_sort(arr, 0, len(arr))

def __quick_sort(arr, start_index, end_index):
    if (end_index - start_index) > 1:
        partition = __partition(arr, start_index, end_index)
        __quick_sort(arr, start_index, partition)
        __quick_sort(arr, partition + 1, end_index)

def __partition(arr, n_from, n_to):
    pivot = n_from + random.randint(0,(n_to - (n_from+1)))
    __swap(arr, n_from, pivot)
    value = arr[n_from]
    bigger_index = n_from + 1
    lower_index = n_to - 1
    condition = True
    while condition:
        while bigger_index <= lower_index and arr[bigger_index] <= value:
            bigger_index += 1
        while arr[lower_index] > value:
            lower_index -= 1
        if bigger_index < lower_index:
            __swap(arr, bigger_index, lower_index)
        else:
            condition = False
    __swap(arr, lower_index, n_from)
    return lower_index



def __swap(arr, left, right):
    if left != right:
        arr[left], arr[right] = arr[right], arr[left]

def test():
    i_arr1=[9, 12, 53, 2, 1, 15, 6, 52, 15, 24, 75, 3, 82, 45, 14, 75, 4]
    i_arr2=[]
    i_arr3=[1,2,3,4,5,6,7]
    i_arr4=['a', 't', 's', 'b', 'g']
    i_arr5=["cat", "mouse", "dog", "hamster", "fish"]
    i_arr6=[5.8, 47.2, 0, 65.57, 14.40, 14.4]
    i_arr=[i_arr1, i_arr2, i_arr3, i_arr4, i_arr5, i_arr6]
    q_arr=[]
    for i in range(len(i_arr)):
        q_arr.append(i_arr[i][:])
    print("~~~~~~Insersort~~~~~~")
    for i in range(len(i_arr)):
        print("before:", i_arr[i])
        insert_sort(i_arr[i])
        print("after:", i_arr[i])
    print("\n\n~~~~~~Quicksort~~~~~~")
    for i in range(len(q_arr)):
        print("before:", q_arr[i])
        quick_sort(q_arr[i])
        print("after:", q_arr[i])

if __name__ == "__main__":
    test()

