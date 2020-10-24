#!/usr/bin/python
import sys


if __name__ == "__main__":
    args = sys.argv[1:]
    for row in [x.strip("\n") for x in sys.stdin]:
        for arg in args:
            if arg in row:
                print(row)
                