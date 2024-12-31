import heapq


def read_input():
    with open("qsumci.in", "r") as inp:
        n, m = map(int, inp.readline().split())
        p = list(map(int, inp.readline().split()))
        t = list(map(int, inp.readline().split()))
    return n, m, p, t


def write_output(res, s):
    with open("qsumci.out", "w") as out:
        out.write(str(res) + "\n")
        out.write("\n".join(f"{mi} {si}" for mi,si in s))


def solve():
    n, m, p, t = read_input()
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
    
    write_output(C, res)


if __name__ == "__main__":
    solve()
