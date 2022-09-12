from numpy import character

from ..DataStructures.Trie import Trie
# from DataStructures.Trie import Trie

class GraphSearcher():

  def __init__(self, graph, tokenIndexName, stopList = set()) -> None:
    self.graph = graph
    self.tokenIndexName = tokenIndexName
    self.stopList = stopList
    self.trailingWildCardTrie = Trie()
    self.leadingWildCardTrie = Trie()


  def getKeysFromTrailingWildCard(self, preWildCardValue):
    if self.trailingWildCardTrie.keyCount == 0:
      tokens = self.graph.tokenIndex.getTokens()

      for token in tokens:
        charArray = list(token["value"])
        self.trailingWildCardTrie.addKeys(charArray, token["_id"])
    return self.trailingWildCardTrie.evaluateKeys(list(preWildCardValue))


  def getKeysFromLeadingWildCard(self, postWildCardValue):
    if self.leadingWildCardTrie.keyCount == 0:
      tokens = self.graph.tokenIndex.getTokens()

      for token in tokens:
        charArray = list(token["value"]).reverse()
        self.leadingWildCardTrie.addKeys(charArray, token["_id"])
    return self.leadingWildCardTrie.evaluateKeys(list(postWildCardValue).reverse())


  def getMatches(self, key):
    success, values = self.graph.verticesByTokenId.tryGetValuesByKey(key)

    if not success:
      return None

    return values








