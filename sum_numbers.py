import sys


def is_number(arg):
    try:
        float(arg)
        return True
    except ValueError:
        return False


result = 0.0
while True:
    try:
        input_nums = input()
        for num in input_nums.split():
            if is_number(num):
                result = result + float(num)
    except Exception:
        break
print(result)
