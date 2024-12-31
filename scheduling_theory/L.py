import sys
from collections import deque, defaultdict


def create_schedule(deadlines, m, from_to, to_from):
    n = len(deadlines)
    index = next(i for i in range(n) if i not in from_to)

    queue = deque([index])
    while queue:
        j = queue.popleft()
        for k in to_from.get(j, []):
            deadlines[k] = min(deadlines[k], deadlines[j] - 1)
            queue.append(k)

    f = 0
    r = [0] * n
    q = [0] * n
    x = [0] * n

    for i in sorted(range(n), key=lambda idx: deadlines[idx]):
        t = max(r[i], f)
        x[i] = t
        q[t] += 1

        if q[t] == m:
            f = t + 1

        if i in from_to:
            j = from_to[i]
            r[j] = max(r[j], t + 1)

    l_max = max(c + 1 - d for d, c in zip(deadlines, x))
    return l_max, x


def main():
    file_name = "pintreep1l"
    sys.stdin = open(file_name + ".in", "r")
    sys.stdout = open(file_name + ".out", "w")
    n, m = map(int, input().split())
    deadlines = list(map(int, input().split()))

    from_to = {}
    to_from = defaultdict(list)
    for i in range(n - 1):
        x, y = map(int, input().split())
        from_to[x - 1] = y - 1
        to_from[y - 1].append(x - 1)

    l_max, schedule = create_schedule(deadlines, m, from_to, to_from)

    print(l_max)
    print(*schedule)

if __name__ == "__main__":
    main()