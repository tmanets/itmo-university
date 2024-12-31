import heapq
import sys


def solve(n, jobs):
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

    return len(heap), res


def main():
    file_name = "p1sumu"
    sys.stdin = open(file_name + ".in", "r")
    sys.stdout = open(file_name + ".out", "w")
    n = int(input())
    jobs = [(*map(int, input().split()), i) for i in range(n)]
    m, res = solve(n, jobs)
    print(m)
    print(*res)


if __name__ == "__main__":
    main()
