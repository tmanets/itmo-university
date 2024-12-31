with open('rosalind_ba9o.txt') as f:
    text = f.readline().strip()
    patterns = f.readline().strip().split()
    d = int(f.readline())
#just for memes
#sorry if it is unreadable
print(' '.join(map(str, sorted(sum([[i for i, kmer in [(i, text[i:i+len(pattern)]) for i in range(len(text) - len(pattern) + 1)] if sum(c1 != c2 for c1, c2 in zip(pattern, kmer)) <= d ] for pattern in patterns], [])))))
