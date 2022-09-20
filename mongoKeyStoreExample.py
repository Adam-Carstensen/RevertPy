from Indexing.MongoKeyStore import MongoKeyStore

keyStore = MongoKeyStore("mongodb://localhost:27017", "MongoIndexingExamples", "KeyStoreTest")

keys = [ "Key One", 2, ("Key", 3)]
for key in keys:
  keyStore.add(key)

returnValue = keyStore.get("Key One")
print(returnValue)

returnValue = keyStore.get("Key 2")
print(returnValue)

returnValue = keyStore.get(2)
print(returnValue)
