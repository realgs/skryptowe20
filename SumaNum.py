numbers = []
SEP = '\t'

while True:
  try:
    line = input()
    seperated = line.split(SEP)
    for x in seperated:
      try:
        number = float(x)
        numbers.append(number)
      except Exception:
        pass
  except EOFError:
    print(sum(numbers))
    break
