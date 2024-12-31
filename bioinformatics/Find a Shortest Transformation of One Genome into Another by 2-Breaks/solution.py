from collections import deque
input_file = "rosalind_ba6d.txt"
with open(input_file) as f:
    data = f.readlines()
gen1 = list(map(int, data[0].strip()[1:-1].split()))
gen2 = list(map(int, data[1].strip()[1:-1].split()))
def headtail(x):
    head = str(abs(x)) + 'h'
    tail = str(abs(x)) + 't'
    return (head, tail) if x > 0 else (tail, head)
def construct_graph(gen):
    genome = {}
    end, v = headtail(gen[0])
    for i in gen:
        head, tail = headtail(i)
        genome[v] = head
        v = tail
    genome[v] = end
    return genome
dotted = construct_graph(gen1)
target = construct_graph(gen2)
path = [dotted]
target_edges = sorted(target.items())
def make_non_oriented_graph(g):
    gr = {u:v for v,u in g.items()}
    gr.update(g)
    return gr
target_graph = make_non_oriented_graph(target)
while make_non_oriented_graph(path[-1]) != target_graph:
    g = path[-1].copy()
    complementary_edge = []
    for v, u in target_edges:
        if (v in g and g[v] == u) or (u in g and g[u] == v):
            continue
        for x, y in g.copy().items():
            if v == x or u == x:
                del g[x]
                complementary_edge.append(y)
            if v == y or u == y:
                del g[x]
                complementary_edge.append(x)
        if complementary_edge:
            break
    g[complementary_edge[0]] = complementary_edge[1]
    g[v] = u
    path.append(g)
def graph_to_genome(g):
    gr = make_non_oriented_graph(g)
    q = deque(v for v in gr.keys())
    genome = []

    while q:
        seq = []
        v = q[0]
        while not seq or int(gr[v][:-1]) != abs(int(seq[0])):
            u_val, u_type = gr[v][:-1], gr[v][-1]
            v = u_val + ('t' if u_type == 'h' else 'h')
            seq.append('-'+u_val if u_type == 't' else '+'+u_val)
            q.remove(u_val + u_type)
            q.remove(v)
        genome.append('(' + ' '.join(seq) + ')')
    return ''.join(genome)
print('\n'.join([graph_to_genome(graph) for graph in path]))
