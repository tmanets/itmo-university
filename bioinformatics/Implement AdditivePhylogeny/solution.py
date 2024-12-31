def get_path(graph, src, dst, visited):
    visited[src] = True
    for v, w in graph[src]:
        if visited[v]:
            continue
        if v == dst:
            return [(src, w), (dst, 0)]
        path = get_path(graph, v, dst, visited)
        if path is not None:
            return [(src, w)] + path
    return None

def additive_phylogeny(matrix, n, nodeName):
    if n == 2:
        distance = matrix[0][1]
        return {0:[(1, distance)], 1:[(0, distance)]}
    limbLength = min(matrix[i][n-1] + matrix[k][n-1] - matrix[i][k] for i in range(n) for k in range(n) if i != n-1 and k != n-1) // 2
    for i in range(n-1):
        matrix[i][n-1] -= limbLength
        matrix[n-1][i] = matrix[i][n-1]
    for i in range(n-1):
        for j in range(i+1, n-1):
            if matrix[i][j] == matrix[i][n-1] + matrix[j][n-1]:
                x = matrix[i][n-1]
                src, dst = i, j
                break
    graph = additive_phylogeny(matrix, n - 1, nodeName - 1)
    visited = [False] * (2 * len(matrix))
    path = get_path(graph, src, dst, visited)
    curr = 0
    edgeLength = path[0][1]
    remainingLength = x
    while remainingLength >= edgeLength:
        remainingLength -= edgeLength
        curr += 1
        edgeLength = path[curr][1]
    currNode = path[curr][0]
    nextNode = path[curr+1][0]
    graph[currNode].append((nodeName, remainingLength))
    graph[nextNode].append((nodeName, edgeLength - remainingLength))
    graph[nodeName] = [(currNode, remainingLength), (nextNode, edgeLength - remainingLength)]
    for i, (neighbor, _) in enumerate(graph[currNode]):
        if neighbor == nextNode:
            del graph[currNode][i]
            break
    for i, (neighbor, _) in enumerate(graph[nextNode]):
        if neighbor == currNode:
            del graph[nextNode][i]
            break
    graph[n-1] = [(nodeName, limbLength)]
    graph[nodeName].append((n-1, limbLength))
    return graph


input_file = "rosalind_ba7c.txt"
with open(input_file,'r') as f:
    n = int(f.readline())
    matrix = [list(map(int,row.split())) for row in f.readlines()]
graph = additive_phylogeny(matrix, n, 2 * len(matrix) - 3)
for src in graph:
    for dst, length in graph[src]:
        print('%d->%d:%d' % (src, dst, length))
