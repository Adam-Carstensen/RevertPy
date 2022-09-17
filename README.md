# RevertPy

Python port of Revert Libraries

Trie DataStructure

MongoRecordIndex
MongoKeyStore 
MongoKeyValueStore
MongoKeyMultiValueStore

Graph [Under Construction]
GraphSearcher [Under Construction]

SimpleTokenizer


# RevertPy.DataStructures.Trie

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
This returns a Tuple<bool, list[object]>.

```
success, values = trie.evaluateKeys(["I'm", "feeling"])
print(f"{success}: {values}")
```
True: [10.0, -10.0]

Just the words "I'm feeling" match "I'm feeling great", and "I'm feeling terrible", if we don't require a full match. 

```
success, values = trie.evaluateKeys(["feeling", "great"])
print(f"{success}: {values}")
```
True: [10.0]

However, the words "feeling great" only match "I'm feeling great", if we don't require a full match.

```
success, values = trie.evaluateKeys(["I'm", "feeling", "fine"])
print(f"{success}: {values}")
```
True: [0.0, 2.0]

Searching for the full match "I'm feeling fine", returns both of the values which were inserted for that key array.


