def solve():
    with open("f2cmax.in", "r") as inp:
        n = int(inp.readline())
        p = [list(map(int,inp.readline().split())), list(map(int,inp.readline().split()))]
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
    with open("f2cmax.out", "w") as out:
        out.write(str(C2) + "\n")
        out.write(" ".join(map(str, res)) + "\n")
        out.write(" ".join(map(str, res)))

if __name__ == "__main__":
    solve()