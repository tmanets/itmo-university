import sys


def solve(n, d1, d2, a, b, c, d):
    num = [0] * (n + 2)
    time = 0

    if d1 - 1 >= n:
        time += 1
    elif d1 > 0:
        num[d1] += 1

    if d2 - 1 >= n:
        time += 1
    elif d2 > 0:
        num[d2] += 1

    for i in range(n - 2):
        d3 = (a * d1 + b * d2 + c) % d
        d1 = d2
        d2 = d3

        if d3 - 1 >= n:
            time += 1
        else:
            num[d3] += 1

    current_number = 0
    for i in range(1, n + 1):
        current = min(i - current_number, num[i])
        current_number += current
        time += current

    return time


def main():
    file_name = "p1p1sumu"
    sys.stdin = open(file_name + ".in", "r")
    sys.stdout = open(file_name + ".out", "w")

    n, d1, d2, a, b, c, d = map(int, input().split())
    
    time = solve(n, d1, d2, a, b, c, d)
    
    print(time)


if __name__ == "__main__":
    main()
