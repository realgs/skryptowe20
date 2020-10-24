#!/usr/bin/python
import sys


if __name__ == "__main__":
    total_sum = 0
    for number in [x.strip("\n") for x in sys.stdin]:
        try:
            total_sum += float(number)
        except ValueError:
            pass
    print(total_sum)
    