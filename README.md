# RevertPy

Python port of Revert Libraries

Graph [Under Construction]
GraphSearcher [Under Construction]

## RevertPy.Indexing.MongoRecordIndex.py

Used for storing and managing dictionary objects in MongoDB.

For example, a new record can be saved into MongoDB with the following code:
```
from Indexing.MongoRecordIndex import MongoRecordIndex

testRecord = {
                "Key" : "Testing",
                "Value" : 
                { 
                  "First Name" : "John", 
                  "Last Name" : "Doe" 
                } 
              }

recordIndex = MongoRecordIndex("mongodb://localhost:27017", "MongoIndexingTests", "RecordIndexTest")
recordIndex.add(testRecord)
```

After your MongoRecordIndex is populated with data, you can query it using the find function.
```
from Indexing.MongoRecordIndex import MongoRecordIndex

recordIndex = MongoRecordIndex("mongodb://localhost:27017", "DatabaseName", "CollectionName")

#returns a pymongo Cursor object, which you can iterate
findResult = recordIndex.find({ "Key": "Testing"})

for item in findResult:
  print(item)
```

## RevertPy.Indexing.MongoKeyStore.py

Used for storing individual distinct values and checking for their presence.

For example, some misc keys can be saved into MongoDB with the following code:
```
from Indexing.MongoKeyStore import MongoKeyStore

keys = [ "Key One", 2, ("Key", 3)]

keyStore = MongoKeyStore("mongodb://localhost:27017", "MongoIndexingTests", "KeyStoreTest")

for key in keys:
  keyStore.add(key)
```

Notice how the different types are stored with no problems.
Querying for existing keys in the store is as easy as using get and checking for None.
```
from Indexing.MongoKeyStore import MongoKeyStore

keyStore = MongoKeyStore("mongodb://localhost:27017", "MongoIndexingTests", "KeyStoreTest")

returnValue = keyStore.get("Key One")
print(returnValue)
```
> {'_id': ObjectId('6329a7154347467af253f0d0'), 'key': 'Key One'}
```
returnValue = keyStore.get("Key 2")
print(returnValue)
```
> None
```
returnValue = keyStore.get(2)
print(returnValue)
```
> {'_id': ObjectId('6329a7154347467af253f0d1'), 'key': 2}

Notice how "Key 2" doesn't match the datatype of the 2nd key, so it returns None, but "Key One", and 2 match existing keys. 


## RevertPy.DataStructures.MongoKeyValueStore.py

Used for storing values associated with a key.  Only one value per key may be stored in this collection.
For multiple values, refer to RevertPy.DataStructures.MongoKeyMultiValueStore.py.

For example, if we wanted to build a program that returned ordinal text for integers, for fun, we could do it with a lookup:
```
from Indexing.MongoKeyValueStore import MongoKeyValueStore

keyValueStore = MongoKeyValueStore("mongodb://localhost:27017", "MongoIndexingTests", "KeyValueStoreTest")

keys = [1, 2, 3, 4, 5]
values = ["First", "Second", "Third", "Fourth", "Fifth"]

for i in range(0, len(keys)):
  keyValueStore.upsert(keys[i], values[i])
```
That inserts the first 5 positive integers and their ordinal spellings.  Notice the use of upsert for insertions and updates.
To fetch an existing record, we use get:
```
from Indexing.MongoKeyValueStore import MongoKeyValueStore
keyValueStore = MongoKeyValueStore("mongodb://localhost:27017", "MongoIndexingTests", "KeyValueStoreTest")

value = keyValueStore.get(4)
print(value)
```
> {'_id': ObjectId('6329c38795ea62dedcac018f'), 'key': 4, 'value': 'Fourth'}

Notice that it returns the full MongoDB record and not just the value.  It's a dictionary, so fetching value is simple:
```
print(value["value"])
```
> Fourth

## RevertPy.Indexing.MongoKeyMultiValueStore.py

Used for storing multiple values associated with a key.

For example, if we wanted to do a token based indexing, we can use a tokenizer and a simple text along with the MongoKeyMultiValueStore:

```
from Indexing.MongoKeyMultiValueStore import MongoKeyMultiValueStore
from Tokenization.SimpleTokenizer import SimpleTokenizer

keyMultiValueStore = MongoKeyMultiValueStore("mongodb://localhost:27017", "MongoIndexingExamples", "KeyMultiValueStoreTest")
tokenizer = SimpleTokenizer()

paragraph0 = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur efficitur pulvinar cursus."
paragraph1 = "Curabitur non placerat purus. In hac habitasse platea dictumst. Cras placerat consequat sapien id ultrices."
paragraph2 = "Aenean quis lorem pharetra purus posuere rutrum. Nulla at porta sapien, feugiat varius nisl."

paragraphs = [paragraph0, paragraph1, paragraph2]
for i in range(0, len(paragraphs)):
  paragraphTokens = tokenizer.getTokens(paragraphs[i])
  for token in paragraphTokens:
    keyMultiValueStore.add(token, i)
```

Now, we have a database entry where you can query for any of the tokens and get their related values:
```
values = keyMultiValueStore.get("platea")
print(values)
```
> [1]

or
```
values = keyMultiValueStore.get("purus")
print(values)
```
> [1, 2]

## RevertPy.DataStructures.Trie.py

Used to search for arrays of values.  For example:

Imagine you were making an app which tracks users' inputs and you wanted to be able to query for some related data.
In our scenario, we'll be doing a really bad sentiment analysis app!

Populate a Trie with calls to addKeys(self, keys, value = None, allowPartial = False)

```
trie = Trie()
trie.addKeys(["I'm", "feeling", "great"], 10.0, allowPartial=True)
trie.addKeys(["I'm", "feeling", "good"], 5.0)
trie.addKeys(["I'm", "feeling", "fine"], 0.0)
trie.addKeys(["I'm", "feeling", "fine"], 2.0)
trie.addKeys(["I'm", "feeling", "bad"], -5.0)
trie.addKeys(["I'm", "feeling", "terrible"], -10.0, allowPartial=True)
```

The use of allowPartial will vary by your use case, but let's look at what it does, by looking at the evaluateKeys method.

This returns a Tuple<bool, list<object>>.

```
success, values = trie.evaluateKeys(["I'm", "feeling"])
print(f"{success}: {values}")
```
> True: [10.0, -10.0]

Just the words "I'm feeling" match "I'm feeling great", and "I'm feeling terrible", if we don't require a full match. 

```
success, values = trie.evaluateKeys(["feeling", "great"])
print(f"{success}: {values}")
```
> True: [10.0]

However, the words "feeling great" only match "I'm feeling great", if we don't require a full match.

```
success, values = trie.evaluateKeys(["I'm", "feeling", "fine"])
print(f"{success}: {values}")
```
> True: [0.0, 2.0]

Searching for the full match "I'm feeling fine", returns both of the values which were inserted for that key array.

## RevertPy.IO.FileIterable.py

Breadth first search of the file system starting at the rootPath and optionally navigating subFolders.
This iterable will return each file matching the file filter.

For example, on Windows, we have a directory with a sub directory and a few files:

```
path = "C:\directory"
fileIterable = FileIterable(path)

for file in fileIterable:
  print(file)
```

> C:\directory\file1.txt

> C:\directory\file2.txt

> C:\directory\subDirectory\subFile1.dat

Now, if we want to limit the results only to our .dat file, we can use the optional fileFilter constructor parameter.

```
path = "C:\directory"
fileIterable = FileIterable(path, fileFilter="*.dat")

for file in fileIterable:
  print(file)
```

> C:\directory\subDirectory\subFile1.dat

## RevertPy.Tokenization.SimpleTokenizer

Used for breaking text into a list of tokens.  SimpleTokenizer doesn't include punctuation, and will cause punctuated words to become multiple tokens.
> "He's" becomes "He" + "s"

Interestingly, the SimpleTokenizer works with a great deal of foreign languages and character sets because it uses Unicode Character Categories.

"Lu" - Uppercase Letter, "Ll" - Lowercase Letter, and "Nd" - Decimal Number

For example, if you want to tokenize a sentence, you could use the code below:
```
from Tokenization.SimpleTokenizer import SimpleTokenizer

tokenizer = SimpleTokenizer()
tokens = tokenizer.getTokens("Lorem ipsum dolor sit amet, consectetur adipiscing elit.")
print(tokens)
```
> ['Lorem', 'ipsum', 'dolor', 'sit', 'amet', 'consectetur', 'adipiscing', 'elit']

