inf = 1000000000
with open("r2cmax.in", "r") as f:
    n = int(f.readline())
    p1 = list(map(int, f.readline().split()))
    p2 = list(map(int, f.readline().split()))
max_time = sum(p1)
last = [0] + [inf] * max_time
cur = [inf] * (max_time + 1)
for i in range(n):
    for j in range(max_time + 1):
        cur[j] = min(last[j] + p2[i], last[j - p1[i]] if j >= p1[i] else inf)
    last, cur = cur, last
ans = min(max(i, e) for i, e in enumerate(last))
with open("r2cmax.out", "w") as f:
    f.write(str(ans))