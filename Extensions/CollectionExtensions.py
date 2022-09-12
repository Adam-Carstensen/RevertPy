def toDiscreteVector(items):
  currentIndex = 0
  values = {}
  for item in items:
    itemIndex = values.get(item, None)
    if itemIndex == None:
      values[item] = currentIndex
      currentIndex += 1

  return values

def extendDiscreteVector(items, values):
  currentIndex = 0
  for item in items:
    itemIndex = values.get(item, None)
    if itemIndex == None:
      values[item] = currentIndex
      currentIndex += 1

  return values

