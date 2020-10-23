import sys

SEP = '\t'

def select_columns(argv):
  try:
    columns = [int(x) for x in argv[1:]]
    for x in columns:
      if x < 1 or x > 4:
        print("Wrong argument", x)
        exit(1)
    return columns
  except Exception:
    print("Wrong arguments")
    exit(1)

def print_columns(columns):
  while True:
    try:
      line = input()
      if line == '':
        break

      product_col = line.split(SEP)
      to_print = ''
      for col in columns:
        to_print = to_print + product_col[col - 1] + SEP
      print(to_print)
    except EOFError:
      break

columns = select_columns(sys.argv)
print_columns(columns)
