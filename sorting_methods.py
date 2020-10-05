def mergesort(list):

  def merge(left, right):
    if not left and not right:
      return []
    elif not right:
      return left
    elif not left:
      return right
    else:
      l = left[0]
      r = right[0]
      if l < r:
        new_list = merge(left[1:], right)
        new_list.insert(0, l)
        return new_list
      else:
        new_list = merge(left, right[1:])
        new_list.insert(0, r)
        return new_list

  splitPoint = len(list) // 2
  if splitPoint == 0:
    return list
  else:
    left, right = list[:splitPoint], list[splitPoint:]
    return merge(mergesort(left), mergesort(right))

def bubblesort(list):
  sorted = False
  while not sorted:
    sorted = True
    for id, x in enumerate(list):
      if id + 1 != len(list) and x > list[id + 1]:
        list[id] = list[id + 1]
        list[id + 1] = x
        sorted = False
  return list
