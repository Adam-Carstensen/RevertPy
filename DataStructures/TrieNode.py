class TrieNode():
  def __init__(self, rootNode = False, key = None, value = None) -> None:
    self.children = {} #dictionary<TKey, TrieNode>
    self.key = key
    self.values = set()
    self.count = 0
    self.rootNode = rootNode
  
  def add(self, trieNode):
    childNode = self.children.get(trieNode.key, None)
    if childNode == None:
      self.children[trieNode.key] = trieNode
    for item in trieNode.values:
      childNode.values.add(item)

  def addKeysAllowPartial(self, keys, value = None):
    self.addKeysByPositionAllowPartial(keys, value, 0)

  def addKeysByPositionAllowPartial(self, keys, value, position):
    self.count += 1

    self.values.add(value)

    if position >= len(keys):
      return

    nextKey = keys[position]

    nextNode = self.children.get(nextKey, None)

    if nextNode == None:
      nextNode = TrieNode(rootNode = False, key = nextKey)
      self.children[nextKey] = nextNode

    # if value != None:
    #   nextNode.values.add(value)
    nextNode.addKeysByPositionAllowPartial(keys, value, position + 1)

  def addKeys(self, keys, value = None):
    self.addKeysByPosition(keys, value, 0)

  def addKeysByPosition(self, keys, value, position):
    self.count += 1
    
    if position >= len(keys):
      if value != None:
        self.values.add(value)
      return
    
    nextKey = keys[position]

    nextNode = self.children.get(nextKey, None)

    if nextNode == None:
      nextNode = TrieNode(rootNode = False, key = nextKey)
      self.children[nextKey] = nextNode

    # if value != None:
    #   nextNode.values.add(value)
    nextNode.addKeysByPosition(keys, value, position + 1)


  def aggregateKeys(self):
    return self.aggregateMoreKeys([])

  def aggregateMoreKeys(self, keys):
    keys.append((self.key, self.count))

    allTrees = []
    if len(self.children) == 0: # or len(keys) >= 3: #TODO: Document why this is >= 3
      allTrees.append(keys)

    for key, child in self.children.items():
      childTrees = child.aggregateMoreKeys(keys)
      allTrees = allTrees + childTrees

    return allTrees

  def tryEvaluate(self, key):
    nextTreeNode = self.children.get(key, None)
    if nextTreeNode == None:
      values = self.getValues()
      if self.rootNode:
        return False, []
      return any(values), list(values)
    return True, nextTreeNode.getValues()


  def getValues(self):
    return self.values
    # self.getMoreValues(values)
    # return values

  def getMoreValues(self, values):
    for key, trieNode in self.children.items():
      trieNode.getMoreValues(values)
    if (len(self.values) != 0):
      for value in self.values:
        values.append(value)
    return values

  def tryEvaluateKeysStrict(self, keys) -> bool:
    return self.__tryEvaluateKeysByPositionStrict(keys, 0, [])

  def __tryEvaluateKeysByPositionStrict(self, keys, position, values) -> bool:
    values = values + list(self.getValues())

    if len(keys) <= position:
      return any(values), values

    currentKey = keys[position]

    nextTreeNode = self.children.get(currentKey, None)
    if nextTreeNode == None:
      return False, []
    
    return nextTreeNode.__tryEvaluateKeysByPositionStrict(keys, position + 1, values)

  

  def tryEvaluateKeys(self, keys) -> bool:
    return self.__tryEvaluateKeysByPosition(keys, 0, [])

  def __tryEvaluateKeysByPosition(self, keys, position, values) -> bool:

    if len(keys) <= position:
      values = values + list(self.getValues())
      return True, values

    currentKey = keys[position]

    nextTreeNode = self.children.get(currentKey, None)
    if nextTreeNode == None:
      if len(values) > 0:
        return True, values
      return False, []
    
    return nextTreeNode.__tryEvaluateKeysByPosition(keys, position + 1, values)

  



