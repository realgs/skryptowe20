import sys
import os

args = sys.argv
nums = [int(arg) for arg in args if arg.isdigit()]

while True:
    it = 0
    try:
        input_line = input()
        for word in input_line.split():
            if it in nums:
                print(word, end='\t')
            it += 1
        print()
    except Exception:
        break
