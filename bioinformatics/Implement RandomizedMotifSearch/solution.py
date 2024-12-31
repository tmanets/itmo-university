from random import randint

N = 1000
inputFile = "rosalind_ba2f.txt"
with open(inputFile) as f:
    data = f.readlines()
k, t = map(int, data[0].split())
Dna = list(map(lambda x: x.strip(), data[1:])) 

def RandomizedMotifSearch():
    motifs = [randomMotif(dna) for dna in Dna]
    bestMotifs = motifs
    while True:
        profile = createProfile(motifs)
        motifs = createMotifs(profile, Dna)
        if score(motifs) < score(bestMotifs):
            bestMotifs = motifs
        else:
            return bestMotifs

def randomMotif(dna):
    x = randint(0, len(dna)-k)
    return dna[x:x+k]

def createProfile(motifs):
    profile = {x:[1 for i in range(k)] for x in "ACGT"}
    for i in range(t):
        for j in range(k):
            profile[motifs[i][j]][j] += 1
    #кажется нет разницы делить или нет, все равно знаменатель никак не участвует далее
    #for x in "ACGT":
    #    for j in range(k):
    #        profile[x][j] /= (t+4)
    return profile

def createMotifs(profile, Dna):
    return [getBestMatch(profile,dna) for dna in Dna]

def getBestMatch(profile, dna):
    def calcProb(pos):
        res = 1
        for i in range(k):
            res *= profile[dna[pos+i]][i]
        return res
    maxProb = 0
    bestPos = 0
    for pos in range(len(dna) - k + 1):
        prob = calcProb(pos)
        if prob > maxProb:
            maxProb = prob
            bestPos = pos
    return dna[bestPos:bestPos+k]
def score(motifs):
    profile = createProfile(motifs)
    res = 0
    for i in range(k):
        max_cnt = max([profile[x][i] for x in profile])
        res += t - max_cnt
    return res

bestMotifs = RandomizedMotifSearch()
for i in range(N):
    motifs = RandomizedMotifSearch()
    if score(motifs) < score(bestMotifs):
        bestMotifs = motifs

for motif in bestMotifs:
    print(motif)
