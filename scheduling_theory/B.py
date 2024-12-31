import sys

def allocate_schedule(schedule, times, indices, init=0):
    total_time = init
    for idx in indices:
        schedule[idx] = total_time
        total_time += times[idx]
    return total_time

def create_schedule(n, a, b):
    group_1 = [idx for idx, v in enumerate(a) if v <= b[idx]]
    group_2 = [idx for idx, v in enumerate(a) if v > b[idx]]

    max_group_1 = max(group_1, key=lambda idx: a[idx], default=None)
    max_group_2 = max(group_2, key=lambda idx: b[idx], default=None)

    if max_group_1 is None or (max_group_2 is not None and a[max_group_1] < b[max_group_2]):
        t, s1, s2 = create_schedule(n, b, a)
        return t, s2, s1
    total_time = max(sum(a), sum(b), max(a[i] + b[i] for i in range(n)))

    schedule_1 = [0] * n
    allocate_schedule(schedule_1, a, [idx for idx in group_1 if idx != max_group_1])
    allocate_schedule(schedule_1, a, [max_group_1], total_time - a[max_group_1])
    allocate_schedule(schedule_1, a, group_2, total_time - a[max_group_1] - sum(a[idx] for idx in group_2))

    schedule_2 = [0] * n
    allocate_schedule(schedule_2, b, [max_group_1])
    allocate_schedule(schedule_2, b, [idx for idx in group_1 if idx != max_group_1], b[max_group_1])
    allocate_schedule(schedule_2, b, group_2, total_time - sum(b[idx] for idx in group_2))

    return total_time, schedule_1, schedule_2

def main():
    file_name = "o2cmax"
    sys.stdin = open(file_name + ".in", "r")
    sys.stdout = open(file_name + ".out", "w")
    
    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    
    c, first_schedule, second_schedule = create_schedule(n, a, b)
    print(c)
    print(*first_schedule)
    print(*second_schedule)

if __name__ == "__main__":
    main()
