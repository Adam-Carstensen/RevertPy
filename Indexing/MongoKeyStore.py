from pymongo import MongoClient, ReturnDocument
import pymongo

class MongoKeyStore():
 
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

  def add(self, key):
    if self.get(key) == None:
      self.collection.insert_one({"key": key })

  def addRange(self, keysToAdd):
    formattedItems = []
    for key in keysToAdd:
      if self.get(key) == None:
        formattedItems.append({"key": key})
    self.collection.insert_many(formattedItems)

  def get(self, key):
    for record in self.collection.find({"key": key}):
      return record

  def getAll(self):
    records = []
    for record in self.collection.find():
      records.append(record)
    return records

  def getCount(self):
    return self.collection.count_documents()

  def getKeys(self):
    keys = []
    for item in self.collection.find():
      keys.append(item["key"])
    return keys

  def deleteAll(self):
    self.collection.delete_many({})

  def delete(self, key):
    deleteResult = self.collection.delete_many({"key": key})
    if (deleteResult.acknowledged == False or deleteResult.deleted_count == 0):
      return False
    return True
      