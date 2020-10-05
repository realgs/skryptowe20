from ArraySorting import SortAlgorithm, Sort

def request_algorithm() -> SortAlgorithm:
    alg = int(input("Select sorting algorithm: \n1. Quick Sort \n2. Insert Sort\n"))
    while alg < 1 or alg > 2:
        print("Unexpected value")
        return request_algorithm()
    return SortAlgorithm(alg)

if __name__ == "__main__":
    arr = [4, -10.2, 0, -1, 3.99, 13, 0, 6.4, 4]
    alg = request_algorithm()
    array_string = lambda x: " ".join(map(str, x))

    print(f"Initial array: [{array_string(arr)}", end="]\n")
    Sort(arr, alg)
    print(f"Sorted array: [{array_string(arr)}", end="]\n")