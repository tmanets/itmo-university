import sys


inf = 1000000000

def solve(n, p1, p2):
    max_time = sum(p1)
    last = [0] + [inf] * max_time
    cur = [inf] * (max_time + 1)
    for i in range(n):
        for j in range(max_time + 1):
            cur[j] = min(last[j] + p2[i], last[j - p1[i]] if j >= p1[i] else inf)
        last, cur = cur, last
    ans = min(max(i, e) for i, e in enumerate(last))    
    return ans


def main():
    file_name = "r2cmax"
    sys.stdin = open(file_name + ".in", "r")
    sys.stdout = open(file_name + ".out", "w")
    n = int(input())
    p1 = list(map(int, input().split()))
    p2 = list(map(int, input().split()))
    ans = solve(n, p1, p2)
    print(ans)


if __name__ == "__main__":
    main()

