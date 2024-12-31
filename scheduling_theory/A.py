import sys
from collections import deque


INF = float('inf')
EPS = 1e-10


class Edge:
    def __init__(self, from_, to, capacity, cost, reverse):
        self.from_ = from_
        self.to = to
        self.capacity = capacity
        self.cost = cost
        self.flow = 0.0
        self.reverse = reverse
    def potential(self):
        return self.capacity - self.flow
    
class Network:
    def __init__(self, size, start=0, finish=None):
        self.size = size
        self.start = start
        self.finish = finish if finish is not None else size - 1
        self.edges = [[] for _ in range(size)]

    def emplace_edge(self, from_, to, capacity, cost):
        forward_edge = Edge(from_, to, capacity, cost, len(self.edges[to]))
        reverse_edge = Edge(to, from_, 0, -cost, len(self.edges[from_]))
        self.edges[from_].append(forward_edge)
        self.edges[to].append(reverse_edge)
    
    def max_flow_min_cost(self):
        flow = 0

        while (parent := self.levit()):
            add_flow = INF
            i = self.finish
            while i != self.start:
                add_flow = min(add_flow, parent[i].potential())
                i = parent[i].from_
            
            flow += add_flow

            i = self.finish
            while i != self.start:
                edge = parent[i]
                edge.flow += add_flow
                self.edges[edge.to][edge.reverse].flow -= add_flow
                i = edge.from_

        return flow

    def levit(self):
        FAR_AWAY = 0
        WAITING = 1
        NEARBY = 2

        parent = [None] * self.size
        vtype = [FAR_AWAY] * self.size
        distance = [INF] * self.size
        distance[self.start] = 0

        deq = deque([self.start])

        while deq:
            from_ = deq.popleft()
            vtype[from_] = NEARBY

            for edge in self.edges[from_]:
                if abs(edge.potential()) >= EPS and distance[edge.to] > distance[edge.from_] + edge.cost:
                    distance[edge.to] = distance[edge.from_] + edge.cost

                    if vtype[edge.to] == FAR_AWAY:
                        deq.append(edge.to)
                    elif vtype[edge.to] == NEARBY:
                        deq.appendleft(edge.to)

                    vtype[edge.to] = WAITING
                    parent[edge.to] = edge

        return parent if distance[self.finish] < INF else None
    

def try_schedule(n, m, p, r, d, s, middle):
    boundaries = [(r[i], d[i] + middle) for i in range(n)]
    tmp = sorted(sum(boundaries,()))
    intervals = sorted(set(tmp))
    size = len(intervals)
    net = Network(2 + size - 1 + (size - 1) * m + n, 0, 1)
    machine_sum = sum(s)

    for i in range(2, size + 1):
        net.emplace_edge(i, 1, machine_sum * intervals[i - 1] - intervals[i - 2], 0)
    
    for i in range(1, size):
        for j in range(m):
            capacity = (intervals[i] - intervals[i - 1]) * (j + 1)
            capacity *= s[j] if j == m - 1 else s[j] - s[j + 1]
            net.emplace_edge((size + 1) + j + (i - 1) * m, i + 1, capacity, 0)

    for i in range(n):
        from_ = 2 + size - 1 + m * (size - 1) + i
        net.emplace_edge(0, from_, p[i], 0)
        
        time_index = next(j for j, interval in enumerate(intervals, 1) if boundaries[i][0] <= interval)

        while time_index < size and boundaries[i][1] >= intervals[time_index]:
            for j in range(m):
                capacity = (intervals[time_index] - intervals[time_index - 1])
                capacity *= s[j] if j == m - 1 else s[j] - s[j + 1]
                net.emplace_edge(from_, (2 + size - 1) + (time_index - 1) * m + j, capacity, 0)
            time_index += 1

    return net.max_flow_min_cost()

    
def create_schedule(n, m, p, r, d, s):
    total = sum(p)
    left, right = 0, total
    for _ in range(37):
        middle = (left + right) / 2.
        if abs(try_schedule(n, m, p, r, d, s, middle) - total) <= EPS:
            right = middle
        else:
            left = middle
    return (left + right) / 2.


def main():
    file_name = "cheese"
    sys.stdin = open(file_name + ".in", "r")
    sys.stdout = open(file_name + ".out", "w")
    n, m = map(int, input().split())
    p, r, d = map(list,zip(*[map(int,input().split()) for i in range(n)]))
    s = sorted([int(input()) for _ in range(m)], reverse=True)
    print(create_schedule(n, m, p, r, d, s))

    
if __name__ == "__main__":
    main()
