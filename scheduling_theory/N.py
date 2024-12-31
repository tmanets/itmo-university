import sys


def solve(n, p):
    l = []
    r = []
        
    sorted_p = sorted([(p[0][i], i, 0) if p[0][i] < p[1][i] else (p[1][i], i, 1) for i in range(n)], key=lambda x: x[0])
    for _, i, j in sorted_p:
        if j == 0:
            l.append(i + 1)
        else:
            r.append(i + 1)
    res = l + list(reversed(r))
    C1, C2 = 0, 0
    for i in res:
        t1, t2 = p[0][i - 1], p[1][i - 1]
        C1 += t1
        C2 = max(C1, C2) + t2

    return C2, res


def main():
    file_name = "f2cmax"
    sys.stdin = open(file_name + ".in", "r")
    sys.stdout = open(file_name + ".out", "w")
    
    n = int(input())
    p = [list(map(int,input().split())), list(map(int,input().split()))]
    C2, res = solve(n, p)
    print(C2)
    print(*res)
    print(*res)


if __name__ == "__main__":
    main()
