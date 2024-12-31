def pattern_matching_with_suffix_array(seq, pattern, sa):
    minI = 0
    maxI = len(seq)
    while minI < maxI:
        midI = (minI + maxI) // 2
        if pattern > seq[sa[midI] :][: len(pattern)]:
            minI = midI + 1
        else:
            maxI = midI
    first = minI
    maxI = len(seq)
    while minI < maxI:
        midI = (minI + maxI) // 2
        if pattern < seq[sa[midI] :][: len(pattern)]:
            maxI = midI
        else:
            minI = midI + 1
    last = maxI
    return [] if first > last else list(range(first, last))

input_file = "rosalind_ba9h.txt"
with open(input_file) as f:
    seq = f.readline()
    patterns = list(map(lambda x: x.strip(), f.readlines()))
seqs = dict((i, seq[i:]) for i in range(len(seq)))
sa = sorted(seqs.keys(), key=lambda x: seqs[x])
inds = []
for p in patterns:
    for ind in pattern_matching_with_suffix_array(seq, p, sa):
        inds += [sa[ind]]
print(*sorted(set(inds)))
