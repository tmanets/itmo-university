import sys
from functools import partial
import math
 
 
def create_schedule(n, times, funs, prec):
    children = [0] * n
    for row in prec:
        for i in row:
            children[i] += 1
 
    excluded = set(range(n))
    p = sum(times)
    reverse_schedule = [0] * n
 
    for k in range(n - 1, -1, -1):
        j = min((i for i in excluded if children[i] == 0), key=lambda i: funs[i](p))
        excluded.remove(j)
        reverse_schedule[k] = j
        p -= times[j]
 
        for i in prec[j]:
            children[i] -= 1
 
    schedule = [0] * n
    total_time = 0
    for it in reverse_schedule:
        schedule[it] = total_time
        total_time += times[it]
 
    f_max_min = max((funs[i](schedule[i] + times[i]) for i in range(n)), default=0)
 
    return f_max_min, schedule
 
 
def polynomial_function(x, coefficients):
    result = 0
    for coeff in coefficients:
        result = result * x + coeff
    return result
    # return sum(coefficients[i] * (x ** (m - i)) for i in range(m + 1))
 
 
def main():
    file_name = "p1precfmax"
    sys.stdin = open(file_name + ".in", "r")
    sys.stdout = open(file_name + ".out", "w")
    
    data = sys.stdin.read().split()
    index = 0
    n = int(data[index])
    index += 1
    p = list(map(int, data[index:index + n]))
    index += n
    funcs = []
    for i in range(n):
        m = int(data[index])
        index += 1
        coefs = list(map(int, data[index:index + m + 1]))
        index += m + 1
        funcs.append(partial(polynomial_function, coefficients=coefs))
    d = int(data[index])
    index += 1
    prec = [[] for _ in range(n)]
    for i in range(d):
        from_idx = int(data[index]) - 1
        to_idx = int(data[index + 1]) - 1
        index += 2
        prec[to_idx].append(from_idx)
     
    f_max_min, schedule = create_schedule(n, p, funcs, prec)
    print(f_max_min)
    print(*schedule)
 
if __name__ == "__main__":
    main()