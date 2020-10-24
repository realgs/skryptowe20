import sys

args = sys.argv
if len(args) > 0:
    while True:
        try:
            input_line = input()
            for word in input_line.split():
                if word in args:
                    print(input_line)
        except Exception:
            break
