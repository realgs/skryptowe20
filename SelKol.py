#!/usr/bin/python
import sys


def interpret_stdin(stdinputs):
    columns = {1: [], 2: [], 3: [], 4: []}
    for i, line in enumerate(stdinputs):
        data = line.split()
        date, name, weight, price = data
        columns[1].append(date)
        columns[2].append(name)
        columns[3].append(weight)
        columns[4].append(price)
    return columns


def print_columns(columns_numbers, columns):
    output = ""
    for i in range(len(columns[1])):
        for col_number in columns_numbers:
            output += columns[int(col_number)][i] + "\t"
        output += "\n"
    print(output)


if __name__ == "__main__":
    columns = interpret_stdin([x.strip("\n") for x in sys.stdin])
    print_columns(sys.argv[1:], columns)
