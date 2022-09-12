from .TrieNode import TrieNode

class Trie():
  def __init__(self) -> None:
    self.rootNode = TrieNode(rootNode = True)
    self.keyCount = 0
   

  def getNodes(self):
    nodes = []
    for child in self.rootNode.children.values:
      nodes.append(child)
    return nodes


  def aggregateKeys(self):
    allTrees = []

    for key, trieNode in self.rootNode.children.items():
      childTrees = trieNode.aggregateKeys()
      if (childTrees != None):
        allTrees = allTrees + childTrees
    
    return allTrees

  
  def addKeys(self, keys, value = None, allowPartial = False):
    """If allowPartial = True, it allows for partial key array matches to bring back results 
    in evaluate and evaluateKeys"""

    if allowPartial:
      self.keyCount += len(keys)
      for i in range(0, len(keys)):
        keyArray = keys[i:]
        self.rootNode.addKeysAllowPartial(keyArray, value)       
    else:
      self.keyCount += len(keys)
      self.rootNode.addKeys(keys, value)

  def contains(self, keys):
    return self.rootNode.tryEvaluateKeys(keys)

  def evaluate(self, key):
    """returns a Tuple<bool, [values]>"""
    return self.rootNode.tryEvaluate(key)

  def evaluateKeys(self, keys):
    """returns a Tuple<bool, [values]>"""
    allValues = set()
    for i in range(0, len(keys)):
      (success, values) = self.rootNode.tryEvaluateKeys(keys[i:])
      if success:
        for value in values:
          allValues.add(value)
    return (len(allValues) > 0, list(allValues))

  def evaluateKeysStrict(self, keys):
    """returns a Tuple<bool, [values]>"""
    (success, values) = self.rootNode.tryEvaluateKeysStrict(keys)
    return (success, list(values))
