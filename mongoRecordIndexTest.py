from Indexing.MongoRecordIndex import MongoRecordIndex

testRecord = {
                "Key" : "Testing",
                "Value" : 
                { 
                  "First Name" : "John", 
                  "Last Name" : "Doe" 
                } 
              }

recordIndex = MongoRecordIndex("mongodb://localhost:27017", "DatabaseName", "CollectionName")

recordIndex.add(testRecord)

#returns a pymongo Cursor object, which you can iterate
findResult = recordIndex.find({ "Key": "Testing"})

for item in findResult:
  print(item)


