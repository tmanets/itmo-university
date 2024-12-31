import heapq
import sys


def solve(n, jobs):
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

    return sumwu, res

def main():
    file_name = "p1sumwu"
    sys.stdin = open(file_name + ".in", "r")
    sys.stdout = open(file_name + ".out", "w")
    n = int(input())
    jobs = [(*map(int, input().split()), i) for i in range(n)]
    sumwu, res = solve(n, jobs)
    print(sumwu)
    print(*res)


if __name__ == "__main__":
    main()

