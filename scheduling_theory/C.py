import sys
import heapq
from collections import defaultdict


class DisjointSets:
    def __init__(self, n):
        self.parent = list(range(n))

    def find(self, i):
        if self.parent[i] != i:
            self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def unite(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x != root_y:
            self.parent[root_x] = root_y


def create_schedule(old_times, old_weights, outree):
    n = len(old_times)
    weights = old_weights[:]
    times = old_times[:]
    sequences = list(range(n))

    parents = {}
    children = set()
    for v, u in outree:
        parents[v] = u
        children.add(v)

    root = next(i for i in range(n) if i not in children)

    metrics = [weights[i] / times[i] for i in range(n)]
    current_version = [0] * n 
    sets = DisjointSets(n)

    heap = [(-metrics[i], i, 0) for i in range(n) if i != root]
    heapq.heapify(heap)

    while heap:
        _, j, version = heapq.heappop(heap)
        if version != current_version[j]:
            continue

        if j not in parents:
            continue

        i = sets.find(parents[j])
        weights[i] += weights[j]
        times[i] += times[j]

        metrics[i] = weights[i] / times[i]
        current_version[i] += 1
        heapq.heappush(heap, (-metrics[i], i, current_version[i]))

        parents[j] = sequences[i]
        sequences[i] = sequences[j]
        sets.unite(j, i)

    current = sequences[root]
    schedule_sequence = [current]
    while current in parents:
        current = parents[current]
        schedule_sequence.append(current)

    schedule = [0] * n
    total_time = 0
    sumwc = 0
    for i in reversed(schedule_sequence):
        schedule[i] = total_time
        sumwc += (total_time + old_times[i]) * old_weights[i]
        total_time += old_times[i]

    return sumwc, schedule


def main():
    file_name = "p1outtreewc"
    sys.stdin = open(file_name + ".in", "r")
    sys.stdout = open(file_name + ".out", "w")
    
    n = int(input())
    times = list(map(int, input().split()))
    weights = list(map(int, input().split()))
    outree = [tuple(map(lambda x: int(x) - 1, input().split())) for _ in range(n - 1)]
    
    opt, schedule = create_schedule(times, weights, outree)
    print(opt)
    print(*schedule)


if __name__ == "__main__":
    main()
