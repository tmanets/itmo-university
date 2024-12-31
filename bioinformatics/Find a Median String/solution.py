import itertools

def d_Dna(pattern):
    ans = 0
    for dna in Dna:
        ans += d_Text(pattern, dna)
    return ans

def d_Text(pattern, text):
    min_hd = 1e10
    for i in range(len(text)-k+1):
        pattern1 = text[i:i+k]
        tmp = hamming_distance(pattern, pattern1)
        if tmp < min_hd:
            min_hd = tmp
    return min_hd

def hamming_distance(pattern, pattern1):
    miss = 0
    for i in range(k):
        if pattern[i] != pattern1[i]:
            miss += 1
    return miss

input_file = "rosalind_ba2b.txt"
with open(input_file) as f:
    data = f.readlines()
k = int(data[0])
Dna = list(map(lambda x: x.strip(), data[1:])) 
patterns = sorted(map(''.join, itertools.product('ACTG', repeat=k)))
min_d = 1e10
answer = ''
for pattern in patterns:
    tmp = d_Dna(pattern)
    if tmp < min_d:
        min_d = tmp
        answer = pattern
print(answer)


