import sys

SEP = '\t'

def readInput():
  arr = []
  while True:
    try:
      line = input()
      arr.append(line)
    except EOFError:
      return arr


def existsInArr(string, arr):
  for x in arr:
    if (string.find(x) != -1):
      return True
  return False


arr = readInput()
filtered = filter(lambda x: existsInArr(x, sys.argv), arr)
for x in list(filtered):
  print(x)
