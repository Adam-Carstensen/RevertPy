from DataStructures.Trie import Trie

trie = Trie()
trie.addKeys(["I'm", "feeling", "great"], 10.0, allowPartial=True)
trie.addKeys(["I'm", "feeling", "good"], 5.0)
trie.addKeys(["I'm", "feeling", "fine"], 0.0)
trie.addKeys(["I'm", "feeling", "fine"], 2.0)
trie.addKeys(["I'm", "feeling", "bad"], -5.0)
trie.addKeys(["I'm", "feeling", "terrible"], -10.0, allowPartial=True)

success, values = trie.evaluateKeys(["I'm", "feeling"])
print(f"{success}: {values}")

success, values = trie.evaluateKeys(["feeling", "great"])
print(f"{success}: {values}")

success, values = trie.evaluateKeys(["I'm", "feeling", "fine"])
print(f"{success}: {values}")









