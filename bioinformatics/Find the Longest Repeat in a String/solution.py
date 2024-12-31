def suffix_tree(seq, starts):
    from os.path import commonprefix
    graph = {}
    bases = sorted(set([seq[start] for start in starts]))
    for base in bases:
        matching = [start for start in starts if seq[start] == base]
        seqs = [seq[s:] for s in matching]
        prefix = commonprefix(seqs)
        size = len(prefix)
        new_starts = [start + size for start in matching if start + size < len(seq)]
        graph[prefix] = suffix_tree(seq, new_starts)
    return graph

def dfs(tree):
    for n1 in tree.keys():
        if not len(tree[n1]):
            yield ""
        for n2 in dfs(tree[n1]):
            yield n1 + n2

input_file = "rosalind_ba9d.txt"
seq = open(input_file).read().strip()
tree = suffix_tree(seq, range(len(seq)))
print(max(dfs(tree), key=lambda x: len(x)))
