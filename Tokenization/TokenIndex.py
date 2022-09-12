from bson import ObjectId
from numpy import append
from ..Indexing.MongoRecordIndex import MongoRecordIndex
from ..Tokenization.SimpleTokenizer import SimpleTokenizer

class TokenIndex():

  def __init__(self, connectionString, databaseName, collectionName) -> None:
    self.connectionString = connectionString
    self.databaseName = databaseName
    self.collectionName = collectionName

    self.tokenizer = SimpleTokenizer()
    self.tokenByIdIndex = MongoRecordIndex(connectionString, databaseName, collectionName)
    self.tokenByIdCache = {} # dictionary<ObjectId, {}>
    self.tokenIdByStringIndex = {} # dictionary<str, ObjectId>


    items = self.tokenByIdIndex.getAll()

    for item in items:
      self.tokenByIdCache[item["_id"]] = item
      self.tokenIdByStringIndex[item["value"]] = item["_id"]


  def incrementValue(self, dictionary, key):
    count = dictionary.get(key, 0)
    dictionary[key] = count + 1
    
  def getTokenIDsWithCount(self, value, createNewTokens=True, stopList=None):
    """
      Gets a list of ObjectIds representing Tokens.

      :param str value: the string you're getting tokens from
      :param bool createNewTokens: The recipient of the message
      :param stopList: a Set of strings, lowercased, containing words which shouldn't be considered
      :type priority: Set<str> or None
      :return: list of ObjectId
      """

    tokenStrings = self.tokenizer.getTokens(value)

    countById = {} # dictionary<ObjectId, int>
    newTokens = {} # dictionary<str, {}>

    skippedTokenCount = 0

    for tokenString in tokenStrings:
      lowerString = tokenString.lower()
      if stopList != None and lowerString in stopList:
        skippedTokenCount += 1
        continue
      
      tokenId = self.tokenIdByStringIndex.get(lowerString, None)
      if (tokenId != None):
        self.incrementValue(countById, tokenId)
      else:
        newToken = newTokens.get(lowerString, None)
        if newToken != None:
          self.incrementValue(countById, newToken["_id"])
        elif createNewTokens:
          token = { "_id": ObjectId(), "value": tokenString }
          newToken[lowerString] = token

    if createNewTokens and any(newTokens):
      for key, value in newTokens.items():
        self.incrementValue(countById, value["_id"])
      
      self.bulkInsert(newTokens.values)

    return countById

  def getTokensByIds(self, tokenIds):
    success, items = self.tokenByIdIndex.tryGetItems(tokenIds)
    return items


  def getTokenIdsFromArray(self, tokenStrings):
    tokenIds = []
    for tokenString in tokenStrings:
      tokenId = self.getTokenIds(tokenString)
      tokenIds.append(tokenId)
    return tokenIds
  

  def getTokenIds(self, value, createNewTokens = True, stopList = None):
    if value is None or value.isspace():
      return None
    tokenStrings = self.tokenizer.getTokens(value)

    tokenIds = []
    newTokens = []

    for tokenString in tokenStrings:
      lowerToken = tokenString.lower()
      if tokenString.isspace() or (stopList != None and lowerToken in stopList):
        continue
    
      tokenId = self.tokenIdByStringIndex.get(lowerToken, None)
      if (tokenId != None): 
        tokenIds.append(tokenId)
      else:
        newTokens.append({"value": lowerToken})

    if createNewTokens:
      if any(newTokens):
        self.bulkInsert(newTokens)
      
      for token in newTokens:
        tokenIds.append(token["_id"])

    return tokenIds

  def getTokenId(self, value, createNewToken = False, stopList = None):
    if value is None or value.isspace():
      return None
    
    tokens = self.tokenizer.getTokens(value)
    if len(tokens) > 1:
      raise Exception("Value provided cannot contain more than 1 token.")

    lowerToken = value.lower()

    if value.isspace() or (stopList != None and lowerToken in stopList):
      return None
  
    tokenId = self.tokenIdByStringIndex.get(lowerToken, None)
    if (tokenId != None): 
      return tokenId
    elif createNewToken:
      token = {"_id": ObjectId(), "value": value}
      self.tokenByIdIndex.add(token)
      self.tokenIdByStringIndex[lowerToken] = token["_id"]
      return token
    return None

  def getTokens(self):
    return self.tokenByIdIndex.getAll()
 

  def bulkInsert(self, tokens):
    for token in tokens:
      if "_id" not in token.keys():
        token["_id"] = ObjectId()
      self.tokenIdByStringIndex[token["value"]] = token["_id"]

      # upsert logic relies upon _id, which is being set already for cache speed
      self.tokenByIdIndex.addRange(tokens)




















    










