import heapq

with open("p1sumwu.in", "r") as f:
    n = int(f.readline())
    jobs = [(*map(int, f.readline().split()), i) for i in range(n)]

jobs.sort(key=lambda x: x[0])

heap = []
t = 1
for d, w, i in jobs:
    heapq.heappush(heap, (w, d, i))
    if d >= t:
        t += 1
    else:
        _, _, _ = heapq.heappop(heap)

res = [-1]*n
t = 0

sumwu = sum([x[1] for x in jobs])

for w, d, i in sorted(heap, key= lambda x:x[1]):
    res[i] = t
    sumwu -= w
    t += 1

for k in range(n):
    if res[k] == -1:
        res[k] = t
        t += 1

with open("p1sumwu.out", "w") as f:
    f.write(f"{sumwu}\n")
    f.write(" ".join(map(str, res)))
