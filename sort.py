import argparse
import sorter
ALLOWED_ALGORITHMS = ["quick", "selection"]
parser = argparse.ArgumentParser(description="sort integer array")
parser.add_argument("list", help="list to be sorted", type=float, nargs='+')
parser.add_argument("-m", "--method", help="sorting algorithm to be used", choices=ALLOWED_ALGORITHMS)
args = parser.parse_args()
sorter.sort(args.list, args.method)
print(args.list)
