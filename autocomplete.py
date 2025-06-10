import json

class TrieNode():
    def __init__(self):
        self.children = {}
        self.last = False
        self.word = None

class Trie():
    def __init__(self):
        self.root = TrieNode()
        self.suggestions = []
        self.max_suggestions = 10
        self.frequencies = {}
        self.last_search_metrics = {}

    def formTrie(self, keys):
        for key in keys:
            self.insert(key)

    def insert(self, key):
        node = self.root
        for a in key:
            if not node.children.get(a):
                node.children[a] = TrieNode()
            node = node.children[a]
        node.last = True
        node.word = key

    def suggestionsRec(self, node, word):
        if node.last:
            self.suggestions.append(word)

        for a, n in node.children.items():
            self.suggestionsRec(n, word + a)

    def printAutoSuggestions(self, key):
        node = self.root
        self.suggestions = []
        nodes_traversed = 0

        for a in key:
            if not node.children.get(a):
                self.last_search_metrics = {
                    "prefix": key,
                    "nodes_traversed": nodes_traversed,
                    "suggestions_found": 0,
                    "search_depth": len(key)
                }
                return 0
            node = node.children[a]
            nodes_traversed += 1

        if not node.children:
            self.last_search_metrics = {
                "prefix": key,
                "nodes_traversed": nodes_traversed,
                "suggestions_found": 0,
                "search_depth": len(key)
            }
            return -1

        self.suggestionsRec(node, key)
        
        sorted_suggestions = sorted(
            self.suggestions,
            key=lambda x: self.frequencies.get(x, 0),
            reverse=True
        )
        
        self.last_search_metrics = {
            "prefix": key,
            "nodes_traversed": nodes_traversed,
            "suggestions_found": len(self.suggestions),
            "suggestions_shown": min(len(sorted_suggestions), self.max_suggestions),
            "search_depth": len(key)
        }
        
        for suggestion in sorted_suggestions[:self.max_suggestions]:
            print(suggestion, end=' ')
        print()
        
        return 1

    def get_height(self, node=None):
        if node is None:
            node = self.root
        if not node.children:
            return 0
        return 1 + max((self.get_height(child) for child in node.children.values()), default=0)
    
    def get_total_nodes(self, node=None):
        if node is None:
            node = self.root
        count = 1
        for child in node.children.values():
            count += self.get_total_nodes(child)
        return count
    
    def get_word_count(self):
        def count_words(node):
            count = 1 if node.last else 0
            for child in node.children.values():
                count += count_words(child)
            return count
        return count_words(self.root)

def load_words(trie):
    with open('word_frequencies.json', 'r') as f:
        trie.frequencies = json.load(f)
    
    valid_words = list(trie.frequencies.keys())
    trie.formTrie(valid_words)
    return valid_words

def main():
    trie = Trie()
    print("Loading words...")
    words = load_words(trie)
    
    print("\nTrie details:")
    print(f"Total words loaded: {len(words):,}")
    print(f"Trie height: {trie.get_height()}")
    print(f"Total nodes: {trie.get_total_nodes():,}")
    print(f"Word count: {trie.get_word_count():,}")
    print(f"Memory efficient ratio: {(trie.get_total_nodes() / len(words)):.2f} nodes per word")
    print("-" * 50 + "\n")
    
    while True:
        key = input("Enter a prefix: ")

        if not key:
            break

        result = trie.printAutoSuggestions(key)

        if result == -1:
            print("No suggestions found")
        elif result == 0:
            print("No words found with that prefix")
            
        print("\nSearch metrics:")
        print(f"Prefix length: {trie.last_search_metrics['search_depth']}")
        print(f"Nodes traversed: {trie.last_search_metrics['nodes_traversed']}")
        print(f"Total suggestions found: {trie.last_search_metrics.get('suggestions_found', 0)}")
        if 'suggestions_shown' in trie.last_search_metrics:
            print(f"Suggestions shown: {trie.last_search_metrics['suggestions_shown']}")
        print("-" * 50 + "\n")

if __name__ == "__main__":
    main()