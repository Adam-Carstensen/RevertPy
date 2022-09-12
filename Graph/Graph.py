from bson.objectid import ObjectId

from ..Indexing.MongoKeyMultiValueStore import MongoKeyMultiValueStore
from ..Indexing.MongoRecordIndex import MongoRecordIndex
from ..Tokenization.SimpleTokenizer import SimpleTokenizer

from ..Tokenization.TokenIndex import TokenIndex

from ..MachineLearning.CosineSimilarity import CosineSimilarity
from ..DataStructures.Trie import Trie

class Graph():
  
  def __init__(self, connectionString, databaseName, graphName) -> None:
    self.connectionString = connectionString
    self.databaseName = databaseName
    self.graphName = graphName
    self.tokenIndex = TokenIndex(connectionString, "Graphs", "TokenIndex")
    self.stopList = set()
    self.tokenizer = SimpleTokenizer()

    self.verticesByTokenId = MongoKeyMultiValueStore(connectionString, databaseName, f"{graphName}_VerticesByKey")
    self.vertices = MongoRecordIndex(connectionString, databaseName, f"{graphName}_Vertices")
    self.cliques = MongoRecordIndex(connectionString, databaseName, f"{graphName}_Cliques")

    self.trailingWildCardTrie = Trie()
    self.leadingWildCardTrie = Trie()

  def upsertClique(self, clique):
    """
    Returns the ObjectId of the created Clique
    """

    return self.cliques.upsert(clique)


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


  def getCount(self):
    return self.vertices.getCount()

  def getVertex(self, id):
    return self.vertices.get(id)

  def getVertices(self):
    return self.vertices.getAll()

  def getNeighborIds(self, vertex, includeEdges = True, includeCliques = True):
    if "_id" not in vertex:
      raise Exception("Vertex must be committed to the database to fetch NeighborIds.")    

    entityIds = set()
    if includeCliques:
      if "cliques" in vertex.keys():
        for cliqueId in vertex["cliques"]:
          clique = self.cliques.get(cliqueId)
          if "vertexIds" not in clique: continue
          
          for vertexId in clique["vertexIds"]:
            if vertexId != vertex["_id"]:
              entityIds.append(vertexId)

    if includeEdges:
      if "edges" in vertex.keys():
        for edge in vertex["edges"]:
          entityIds.append(edge["target"])
    
    return list(entityIds)

  def getNeighbors(self, vertex, includeEdges = True, includeCliques = True):
    ids = self.getNeighborIds(vertex, includeEdges, includeCliques)
    neighbors = []
    for id in ids:
      neighbors.append(self.getVertex(id))
    return neighbors

  def upsert(self, vertex, resolveVertex = True):
    if (resolveVertex):
      isOld, resolvedVertex = self.resolveVertex(vertex)

      if isOld:
        resolvedVertex = self.__mergeVertices(resolvedVertex, vertex)
      else:
        resolvedVertex["_id"] = ObjectId()
        if "edges" not in resolvedVertex.keys():
          resolvedVertex["edges"] = []
        if "cliques" not in resolvedVertex.keys():
          resolvedVertex["cliques"] = []

      self.__upsertSearchTokens(resolvedVertex)
      self.vertices.upsert(resolvedVertex["_id"], resolvedVertex)
      return resolvedVertex

    self.__upsertSearchTokens()      
    self.vertices.add(vertex)
    return vertex

  # def update(self, vertex):
  #   if "_id" not in vertex:
  #     return self.add(vertex)

  #   self.__upsertSearchTokens(vertex)
  #   self.vertices.upsert(vertex["_id"], vertex)
  #   return vertex

  # merges vertex2 into vertex1 and returns a new vertex
  def __mergeVertices(self, oldVertex, newVertex):

    features = []
    oldVertexFeatures = {}

    if "features" in oldVertex:
      for feature in oldVertex["features"]:
        featureKey = feature.get("key", None)
        featureValue = feature.get("value", None)
        oldVertexFeatures[(featureKey, featureValue)] = feature

    if "features" in newVertex:
      for feature in newVertex["features"]:
        featureKey = feature.get("key", None)
        featureValue = feature.get("value", None)

        #pop vs get because we don't want to duplicate features
        oldFeature = oldVertexFeatures.pop((featureKey, featureValue), None)

        if oldFeature == None:
          features.append(feature)
        else:
          newFeature = {}
          newFeature["key"] = featureKey
          newFeature["value"] = featureValue

          oldFeatureResolvable = oldFeature.get("resolvable", None)
          newFeatureResolvable = feature.get("resolvable", None)

          if newFeatureResolvable != None:
            newFeature["resolvable"] = newFeatureResolvable
          elif oldFeatureResolvable != None:
            newFeature["resolvable"] = oldFeatureResolvable
          

          oldFeatureSearchable = oldFeature.get("searchable", None)
          newFeatureSearchable = feature.get("searchable", None)        

          if newFeatureSearchable != None:
            newFeature["searchable"] = newFeatureSearchable
          elif oldFeatureSearchable != None:
            newFeature["searchable"] = oldFeatureSearchable

          features.append(newFeature)

    for keyValue, oldFeature in oldVertexFeatures.items():
      features.append({ "key": oldFeature["key"], "value": oldFeature["value"], "searchable": oldFeature.get("searchable", True), "resolvable": oldFeature.get("resolvable", True) })

    edges = []
    oldEdgeByTarget = {}

    if "edges" in oldVertex:
      for edge in oldVertex["edges"]:
        oldEdgeByTarget[edge["target"]] = edge

    if "edges" in newVertex:
      for edge in newVertex["edges"]:
        
        #get vs pop because we DO want to duplicate edges if there is a difference in relationship
        oldEdge = oldEdgeByTarget.get(edge["target"], None)

        if oldEdge == None:
          edges.append(edge)
        else:
          oldEdgeRelationship = oldEdge.get("relationship", None)
          edgeRelationship = edge.get("relationship", None)

          # if relationship is the same, the edge is not duplicated
          if (oldEdgeRelationship == None and edgeRelationship == None) or oldEdgeRelationship == edgeRelationship:
            continue
          
          newEdgeRelationship = edgeRelationship if edgeRelationship != None else oldEdgeRelationship

          newEdge = { "target": edge["target"], "relationship":newEdgeRelationship }
          edges.append(newEdge)

    for target, edge in oldEdgeByTarget.items():
      edges.append(edge)

    cliques = set()
    
    if "cliques" in oldVertex:
      for clique in oldVertex["cliques"]:
        cliques.add(clique)
    
    if "cliques" in newVertex:
      for clique in newVertex["cliques"]:
        cliques.add(clique)

    cliques = list(cliques)

    return { "_id": oldVertex["_id"], "features": features, "edges": edges, "cliques": cliques }


  def __upsertBulkSearchTokens(self, vertices):
    # bulkVerticesByTokenId = {} # dictionary<ObjectId, Set<ObjectId>>
    for vertex in vertices:
      self.__upsertSearchTokens(vertex)


  def __upsertSearchTokens(self, vertex):
      vertexId = vertex["_id"]
      newTokens = set()
      features = vertex["features"]
      searchableFeatures = self.__getSearchableFeatures(features)
      for feature in searchableFeatures:
        for featureName, featureValue in feature.items():
          if isinstance(featureValue, str):
            tokens = self.tokenizer.getTokens(f"{featureName.lower()} {featureValue.lower()}")
            newTokens = newTokens.union(tokens)
          else:
            tokens = self.tokenizer.getTokens(f"{featureName.lower()} {featureValue}")
            newTokens = newTokens.union(tokens)
      
      oldVertex = self.getVertex(vertexId)
      tokensToRemove = []
      tokensToAdd = []

      if oldVertex != None and "features" in oldVertex.keys():
        oldTokens = set()

        oldFeatures = oldVertex["features"]
        oldSearchableFeatures = self.__getSearchableFeatures(oldFeatures)
        for feature in oldSearchableFeatures:
          for featureName, featureValue in feature.items():
            if isinstance(featureValue, str):
              tokens = self.tokenizer.getTokens(f"{featureName.lower()} {featureValue.lower()}")
            else:
              tokens = self.tokenizer.getTokens(f"{featureName.lower()} {featureValue}")

            oldTokens = oldTokens.union(tokens)
            

            for token in tokens:
              if token not in newTokens:
                tokensToRemove.append(token)

        for token in newTokens:
          if token not in oldTokens:
            tokensToAdd.append(token)
      else:
          tokensToAdd = list(newTokens)
      
      for token in tokensToRemove:
        tokenId = self.tokenIndex.getTokenId(token)
        self.verticesByTokenId.delete(tokenId, vertexId)

      for token in tokensToAdd:
        tokenId = self.tokenIndex.getTokenId(token)
        self.verticesByTokenId.add(tokenId, vertexId)


  def resolveVertex(self, vertex):
    isDuplicate, duplicateVertex = self.__isDuplicate(vertex)
    if not isDuplicate or duplicateVertex == None:
      return False, vertex
    
    return True, duplicateVertex


  def calculateFeatureSimilarity(self, vertex1, vertex2) -> float:
    if vertex1["_id"] == vertex2["_id"]:
      return 1.0
    
    if "features" not in vertex1.keys() or vertex1["features"] == None:
      return 0.0

    if "features" not in vertex2.keys() or vertex2["features"] == None:
      return 0.0

    vertex1Features = self.__getResolvableFeatures(vertex1["features"])
    vertex2Features = self.__getResolvableFeatures(vertex2["features"])
    
    vertex1String = ""
    for feature in vertex1Features:
      for key, value in feature.items():
        if vertex1String != "":
          vertex1String += " "
        vertex1String += f"{key} {value}"

    vertex2String = ""
    for feature in vertex2Features:
      for key, value in feature.items():
        if vertex2String != "":
          vertex2String += " "
        vertex2String += f"{key} {value}"
   
    vertex1TokenIds = self.tokenIndex.getTokenIds(vertex1String)
    vertex2TokenIds = self.tokenIndex.getTokenIds(vertex2String)

    countByToken1 = {}
    highestTokenId1 = 0
    for tokenId in vertex1TokenIds:
      count = countByToken1.get(tokenId, 0)
      countByToken1[tokenId] = count + 1
      if tokenId > highestTokenId1:
        highestTokenId1 = tokenId

    countByToken2 = {}
    highestTokenId2 = 0
    for tokenId in vertex2TokenIds:
      count = countByToken2.get(tokenId, 0)
      countByToken2[tokenId] = count + 1
      if tokenId > highestTokenId2:
        highestTokenId2 = tokenId

    highestTokenId = max(highestTokenId1, highestTokenId2)

    vector1 = [0 for i in range(highestTokenId)]
    vector2 = [0 for i in range(highestTokenId)]

    for tokenId, count in countByToken1.items():
      vector1[tokenId] = count

    for tokenId, count in countByToken2.items():
      vector2[tokenId] = count
   
    return CosineSimilarity.getVectorCosineSimilarity(vector1, vector2)



  def __isDuplicate(self, vertex, similarityThreshold = 0.9):
    if "features" not in vertex.keys():
      return False, None
    vertexIds = self.__getVerticesFromFeatures(vertex["features"])

    maxSimilarity = 0.0    
    maxVertex = None
    for vertexIdFromFeatures in vertexIds:
      similarity = self.calculateFeatureSimilarity(vertex, self.getVertex(vertexIdFromFeatures))
      if similarity > maxSimilarity:
        maxSimilarity = similarity
        maxVertex = vertexIdFromFeatures

    if maxVertex != None and maxSimilarity > similarityThreshold:
      return True, self.getVertex(maxVertex)

    return False, None
    
  
    
  def __getVerticesFromFeatures(self, features):
    vertices = []
    vertexIds = set()

    resolvableFeatures = self.__getResolvableFeatures(features)
    featureString = ""
    for feature in resolvableFeatures:
      for key, value in feature.items():
        if featureString != "":
          featureString += " "
        featureString += f"{key} {value}"

    tokenIds = self.tokenIndex.getTokenIds(featureString)
    
    return self.getMatches(tokenIds)

  def getMatches(self, keyVector, intersect = True):
    if keyVector == None or len(keyVector) == 0:
      return None
    
    distinctIds = set()
    distinctMatches = []

    success, id_tokenId_vertexId_Array = self.verticesByTokenId.tryGetValues(keyVector)

    if success:
      for id_tokenId_vertexId in id_tokenId_vertexId_Array:
        if id_tokenId_vertexId["value"] not in distinctIds:
          distinctIds.add(id_tokenId_vertexId["value"])
          distinctMatches.append(id_tokenId_vertexId["value"])

    return distinctMatches


  def calculateFeatureSimilarity(self, vertex1, vertex2) -> float:
    if "_id" in vertex1.keys() and "_id" in vertex2.keys() and vertex1["_id"] == vertex2["_id"]:
      return 1.0
    
    if "features" not in vertex1.keys() or "features" not in vertex2.keys():
      return 0.0

    vertex1Tokens = self.__getResolvableTokenIds(vertex1["features"])
    vertex2Tokens = self.__getResolvableTokenIds(vertex2["features"])

    if vertex1Tokens == None or vertex2Tokens == None or not any(vertex1Tokens) or not any(vertex2Tokens):
      return 0.0

    return self.__calculateTokenArraySimilarity(vertex1Tokens, vertex2Tokens)

  
  def __calculateTokenArraySimilarity(self, tokens1, tokens2):

    tokenLookup = set()
    tokens1Set = set(tokens1)
    tokens2Set = set(tokens2)
    
    for token in tokens1:
      tokenLookup.add(token)

    for token in tokens2:
      tokenLookup.add(token)

    position = 0
    tokens1Vector = [0] * len(tokenLookup)
    tokens2Vector = [0] * len(tokenLookup)

    for item in tokenLookup:
      if item in tokens1Set:
        count1 = tokens1Vector[position]
        tokens1Vector[position] = count1 + 1

      if item in tokens2Set:
        count2 = tokens2Vector[position]
        tokens2Vector[position] = count2 + 1

      position += 1

    return CosineSimilarity.getVectorCosineSimilarity(tokens1Vector, tokens2Vector)


  def toDiscreteVector(self, items):
    values = {}
    for item in items:
      itemIndex = values.get(item, 0)
      values[item] = itemIndex + 1

    vector = []
    for key, count in values.items():
      vector.append(count)

    return vector

    

    

    

  def __getResolvableTokenIds(self, features):
    featureString = ""
    for feature in self.__getResolvableFeatures(features):
      for key, value in feature.items():
        if featureString != "":
          featureString += " "
        featureString += f"{key} {value}"
    tokenIds = self.tokenIndex.getTokenIds(featureString)
    return tokenIds
    


      





  def __getResolvableFeatures(self, features):
    resolvableFeatures = []

    for feature in features:
      # all features are resolvable unless explicitly listed as not resolvable
      if "resolvable" not in feature.keys() or feature["resolvable"]:
        resolvableFeatures.append(feature)
    return resolvableFeatures
    
  def __getSearchableFeatures(self, features):
    searchableFeatures = []
    
    for feature in features:
      # all features are searchable unless explicitly listed as not searchable
      if "searchable" not in feature.keys() or feature["searchable"]:
        searchableFeatures.append(feature)
    return searchableFeatures









  
  

  



