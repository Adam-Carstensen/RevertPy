from Indexing.MongoKeyValueStore import MongoKeyValueStore

keyValueStore = MongoKeyValueStore("mongodb://localhost:27017", "MongoIndexingExamples", "KeyValueStoreTest")

keys = [1, 2, 3, 4, 5]
values = ["First", "Second", "Third", "Fourth", "Fifth"]

for i in range(0, len(keys)):
  keyValueStore.upsert(keys[i], values[i])

value = keyValueStore.get(4)
print(value)

print(value["value"])
