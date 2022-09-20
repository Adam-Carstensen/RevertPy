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

values = keyMultiValueStore.get("platea")
print(values)

values = keyMultiValueStore.get("purus")
print(values)

keyMultiValueStore.deleteAll()