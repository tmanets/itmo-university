import heapq
 
with open("p1sumu.in", "r") as f:
    n = int(f.readline())
    jobs = [(*map(int, f.readline().split()), i) for i in range(n)]
 
jobs.sort(key=lambda x: x[1])
 
heap = []
t = 0
 
for p, d, i in jobs:
    heapq.heappush(heap, (-p, d, i))
    t += p
    if t > d:
        max_p, _, max_i = heapq.heappop(heap)
        t += max_p
 
res = [-1]*n
c = 0
for p, _, i in sorted(heap, key= lambda x:x[1]):
    res[i] = c
    c -= p
 
with open("p1sumu.out", "w") as f:
    f.write(f"{len(heap)}\n")
    f.write(" ".join(map(str, res)))