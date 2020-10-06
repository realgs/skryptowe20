def insert_sort(arr):
    for i in range(1, len(arr)):
        value = arr[i]

        j = i-1
        while j>=0 and value < arr[j]:
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = value

def run():
    arr=[9, 12, 53, 2, 1, 6, 52]
    insert_sort(arr)
    print(arr)

if __name__ == "__main__":
    run()

