import sys
from collections import deque
import math

INF = float('inf')

class Edge:
    def __init__(self, from_, to, capacity, cost, reverse):
        self.from_ = from_
        self.to = to
        self.capacity = capacity
        self.cost = cost
        self.flow = 0
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
        result = []
        min_cost = 0

        while (parent := self.levit()):
            add_flow = INF
            i = self.finish
            while i != self.start:
                add_flow = min(add_flow, parent[i].potential())
                i = parent[i].from_

            i = self.finish
            while i != self.start:
                edge = parent[i]
                edge.flow += add_flow
                self.edges[edge.to][edge.reverse].flow -= add_flow
                result.append(edge)
                min_cost += edge.cost * add_flow
                i = edge.from_

        return min_cost, result

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
                if edge.potential() and distance[edge.to] > distance[edge.from_] + edge.cost:
                    distance[edge.to] = distance[edge.from_] + edge.cost

                    if vtype[edge.to] == FAR_AWAY:
                        deq.append(edge.to)
                    elif vtype[edge.to] == NEARBY:
                        deq.appendleft(edge.to)

                    vtype[edge.to] = WAITING
                    parent[edge.to] = edge

        return parent if distance[self.finish] < INF else None
    

def main():
    file_name = "p1p1sumu"
    sys.stdin = open(file_name + ".in", "r")
    sys.stdout = open(file_name + ".out", "w")

    job_size, machine_size = map(int, input().split())

    times = []
    for _ in range(job_size):
        times.append(list(map(int, input().split())))

    net = Network(2 + job_size + job_size * machine_size, 0, 1)

    for i in range(job_size):
        net.emplace_edge(0, 2 + i, 1, 0)

    for i in range(job_size * machine_size):
        net.emplace_edge(2 + job_size + i, 1, 1, 0)

    for i in range(job_size):
        for j in range(machine_size):
            for k in range(job_size):
                net.emplace_edge(2 + i, 2 + job_size * (j + 1) + k, 1, (k + 1) * times[i][j])

    sum_c, flow = net.max_flow_min_cost()
    result = [[-1] * job_size for _ in range(machine_size)]

    for edge in flow:
        if edge.from_ == 0 or edge.to == 1 or edge.from_ > 2 + job_size - 1 or edge.flow == 0:
            continue

        k = job_size - 1 - (edge.to - 2) % job_size
        j = (edge.to - 2) // job_size - 1
        i = edge.from_ - 2
        result[j][k] = i

    print(sum_c)
    for i in result:
        count = sum(1 for j in i if j != -1)
        print(count, *[j + 1 for j in i if j != -1])


if __name__ == "__main__":
    main()
