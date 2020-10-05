def insert_sort(arr):

    for i in range(len(arr)):
        next_item = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > next_item:
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = next_item
        