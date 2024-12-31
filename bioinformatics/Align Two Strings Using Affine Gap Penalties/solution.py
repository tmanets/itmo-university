with open("BLOSUM62.txt") as f:
    data = f.readlines()
alphabet = data[0].strip().split()
get = lambda c: alphabet.index(c)
matrix = [list(map(int,row.strip().split()[1:])) for row in data[1:]]
openp= 11
exp = 1
inputFile = "rosalind_ba5j.txt"
with open(inputFile) as f:
    data = f.readlines()
str1, str2 = data[0].strip(), data[1].strip()
len1, len2 = len(str1), len(str2)
gm = lambda x1, x2: [[0 for i in range(x2+1)] for j in range(x1+1)]
matrices = {x:gm(len1,len2) for x in ['l','m','u']}
trans = {x:gm(len1,len2) for x in ['l','m','u']}
for i in range(1, len1 + 1):
    for j in range(1, len2 + 1):
        matrices['l'][i][j], trans['l'][i][j] = max((matrices['l'][i-1][j] - exp, ('l', i-1, j)),
                                                    (matrices['m'][i-1][j] - openp,('m' ,i-1, j)))
        matrices['u'][i][j], trans['u'][i][j] = max((matrices['u'][i][j-1] - exp, ('u', i, j-1)),
                                                    (matrices['m'][i][j-1] - openp,('m', i, j-1)))
        matrices['m'][i][j], trans['m'][i][j] = max((matrices['l'][i][j], ('l', i, j)),
                                                    (matrices['m'][i-1][j-1] + matrix[get(str1[i-1])][get(str2[j-1])], ('m', i-1, j-1)),
                                                    (matrices['u'][i][j], ('u', i, j)))
ans1, ans2 = [], []
came_from = trans['m'][len1][len2]
cur_matr = 'm'
while came_from != 0:
    if came_from[0] == 'm' and cur_matr == 'm':
        ans1 = [str1[came_from[1]]] + ans1
        ans2 = [str2[came_from[2]]] + ans2
    elif came_from[0] == 'u':
        ans1 = ["-"] + ans1
        ans2 = [str2[came_from[2]-1]] + ans2
    elif came_from[0] == 'l':
        ans1 = [str1[came_from[1]-1]] + ans1
        ans2 = ["-"] + ans2 
    cur_matr = came_from[0]
    came_from = trans[cur_matr][came_from[1]][came_from[2]]
        
print(matrices['m'][-1][-1])
print("".join(ans1))
print("".join(ans2))
