from pymongo import MongoClient

class MongoRecordIndex():
 
  def __init__(self, connectionString, databaseName, collectionName) -> None:
    self.connectionString = connectionString
    self.databaseName = databaseName
    self.collectionName = collectionName

    self.mongoClient = MongoClient(connectionString)
    self.db = self.mongoClient.get_database(databaseName)
    self.collection = self.db.get_collection(collectionName)


  def find(self, filter):
    return self.collection.find(filter)

  def add(self, item):
    return self.collection.insert_one(item).inserted_id

  def addRange(self, items):
    ids = []
    for item in items:
      if ("_id" in item.keys()):
        ids.append(item["_id"])
    cursor = self.collection.find({"_id": { "$in": ids }})
    values = set()
    for item in cursor:
      values.add(item["_id"])
    
    itemsToAdd = []
    for item in items:
      if ("_id" in item.keys() and item["_id"] not in values):
        itemsToAdd.append(item)

    self.collection.insert_many(itemsToAdd)

  def remove(self, id) -> bool:
    result = self.collection.delete_one({"_id": id})
    return result.acknowledged

  def removeItem(self, item) -> bool:
    result = self.collection.delete_one({"_id": item["_id"]})
    return result.acknowledged

  def removeItems(self, items) -> bool:
    ids = []
    for item in items:
      if (item["_id"] != None):
        ids.append(item["_id"])

    result = self.collection.delete_many({"_id": { "$in": ids}})
    return result.acknowledged

  def update(self, item):
    self.collection.replace_one({"_id": item["_id"]}, item)

  def updateItems(self, items):
    for item in items:
      self.collection.replace_one({"_id", item["_id"]}, item)

  def upsert(self, id, item):
    getResult = self.get(id)
    if (getResult == None):
      self.add(item)
    else:
      self.update(item)

  def upsertItems(self, items):
    ids = []
    for item in items:
      if ("_id" in item.keys()):
        ids.append(item["_id"])

    cursor = self.collection.find({"_id": {"$in": ids}})
    existingItems = set()
    for item in cursor:
      existingItems.add(item["_id"])
    
    for item in items:
      if ("_id" in item.keys() and item["_id"] in existingItems):
        self.update(item)
      else:
        self.add(item)

  def get(self, id):
    cursor = self.collection.find({"_id": id})
    for item in cursor:
      return item

  def getAll(self):
    cursor = self.collection.find()
    items = []
    for item in cursor:
      items.append(item)
    return items

  def tryGet(self, id):
    cursor = self.collection.find({"_id": id})
    returnItem = None
    for item in cursor:
      returnItem = item
  
    return returnItem != None, returnItem

  def tryGetItems(self, ids):
    cursor = self.collection.find("_id", {"$in": ids})
    returnItems = []
    for item in cursor:
      returnItems.append(item)
    return len(returnItems) > 0, returnItems

  def getCount(self):
    return self.collection.count_documents()




      

    