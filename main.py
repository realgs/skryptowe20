from ArraySorting import SortAlgorithm, Sort

def request_algorithm() -> SortAlgorithm:
    alg = int(input("Select sorting algorithm: \n1. Quick Sort \n2. Insert Sort\n"))
    while alg < 1 or alg > 2:
        print("Unexpected value")
        return request_algorithm()
    return SortAlgorithm(alg)

if __name__ == "__main__":
    arr = [4, -10.2, 0, 0, -1, 3.99, 13, 6.4, 4]
    alg = request_algorithm()
    sorted = Sort(arr, alg)
