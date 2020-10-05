def insert_sort(arr):

    for i in range(len(arr)):
        next_item = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > next_item:
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = next_item
        
def bubble_sort(arr):
    swapped = True

    while swapped:
        swapped = False
        for i in range(len(arr)-1):
            if arr[i] > arr[i+1]:
                arr[i], arr[i+1] = arr[i+1], arr[i]
                swapped = True

arr = [5,4,2,5,1,1]
arr2 = [4,2,1,11,23,45,21]
bubble_sort(arr)
insert_sort(arr2)
print(arr)
print(arr2)
                
                
            