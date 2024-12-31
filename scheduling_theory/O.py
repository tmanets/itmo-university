import sys
import heapq


def solve(n, m, p, t):
    queue = [(t[j], 1, j) for j in range(m)]
    heapq.heapify(queue)

    sorted_p = sorted(enumerate(p), key=lambda x: -x[1])
    schedule = [()]*n

    for i in range(n):
        tj, r, j = heapq.heappop(queue)
        index, _ = sorted_p[i]
        schedule[index] = (r, j, index)
        heapq.heappush(queue, (tj + t[j], r + 1, j))
    
    C = 0
    times = [0]*m
    res = [()]*n
    for _, j, index in sorted(schedule, reverse=True):
        res[index] = (j + 1, times[j])
        times[j] += t[j] * p[index]
        C += times[j]

    return C, res


def main():
    file_name = "qsumci"
    sys.stdin = open(file_name + ".in", "r")
    sys.stdout = open(file_name + ".out", "w")

    n, m = map(int, input().split())
    p = list(map(int, input().split()))
    t = list(map(int, input().split()))

    C, res = solve(n, m, p, t)

    print(C)
    for mi, si in res:
        print(mi, si)

if __name__ == "__main__":
    main()
