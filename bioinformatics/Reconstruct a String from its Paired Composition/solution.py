from collections import defaultdict
inputFile = "rosalind_ba3j.txt"
with open(inputFile) as f:
    data = f.readlines()
k, d = map(int, data[0].split())
pairedReads = list(map(lambda x: tuple(x.strip().split('|')), data[1:]))

vertices = set()
graph = defaultdict(list)
for x,y in pairedReads:
    prefix = (x[:-1],y[:-1])
    suffix = (x[1:],y[1:])
    vertices.add(prefix)
    vertices.add(suffix)
    graph[prefix].append(suffix)
indeg = dict.fromkeys(vertices, 0)
outdeg = dict.fromkeys(vertices, 0)
for vertex in vertices:
    if vertex in graph:
        outdeg[vertex] = len(graph[vertex])
        for adj in graph[vertex]:
            indeg[adj] += 1
start = -1
end = -1
for vertex in vertices:
    if indeg[vertex] < outdeg[vertex]:
        start = vertex
    if indeg[vertex] > outdeg[vertex]:
        end = vertex

current_path = [start]
circuit = []
v = start
while len(current_path) > 0:
    if outdeg[v]:
        current_path.append(v)
        nextv = graph[v].pop()
        outdeg[v] -= 1
        v = nextv
    else:
        circuit.append(v)
        v = current_path.pop()

path = circuit[::-1]

xs = ''.join([path[0][0]] + [x[k-2:] for x, y in path[1:]])
ys = ''.join([path[0][1]] + [y[k-2:] for x, y in path[1:]])

print(xs[:d+k] + ys)
