from pymongo import MongoClient, ReturnDocument
import pymongo

class MongoKeyValueStore():
 
  def __init__(self, connectionString, databaseName, collectionName) -> None:
    self.connectionString = connectionString
    self.databaseName = databaseName
    self.collectionName = collectionName

    self.mongoClient = MongoClient(connectionString)
    self.db = self.mongoClient.get_database(databaseName)
    self.collection = self.db.get_collection(collectionName)
    print(self.collection.index_information())
    if len(self.collection.index_information()) <= 1:
       self.collection.create_index([("key", pymongo.DESCENDING)])

  def addRange(self, key, itemsToAdd):
    formattedItems = []
    for item in itemsToAdd:
      formattedItems.append({"key": key, "value": item})
    self.collection.insert_many(formattedItems)

  def upsert(self, key, value):
    if self.get(key) == None:
      self.collection.insert_one({"key": key, "value": value})
    else:
      self.collection.find_one_and_update({"key": key}, { "$set": { "value": value }}, return_document=ReturnDocument.AFTER)

  def get(self, key):
    for value in self.collection.find({"key": key}):
      return value

  def getAll(self):
    return self.collection.find()

  def getCount(self):
    return self.collection.count_documents()

  def getKeys(self):
    keys = []
    for item in self.collection.find():
      keys.append(item["key"])
    return keys

  def getValues(self):
    values = []
    for item in self.collection.find():
      values.append(item["value"])
    return values

  def tryGetValues(self, keys):
    cursor = self.collection.find({"key": { "$in": keys }})
    values = []
    for item in cursor:
      values.append(item)
    success = cursor != None and len(values) != 0
    return success, values

  def deleteAll(self):
    self.collection.delete_many({})

  def delete(self, key):
    deleteResult = self.collection.delete_many({"key": key})
    if (deleteResult.acknowledged == False or deleteResult.deleted_count == 0):
      return False
    return True
      
  def delete(self, key, value):
    deleteResult = self.collection.delete_many({
      "$and": [
        { "key": key},
        { "value": value}
      ]
      })
    if (deleteResult.acknowledged == False or deleteResult.deleted_count == 0):
      return False
    return True