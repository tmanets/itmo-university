from collections import deque

class BitVec:
    BITS = 32

    def __init__(self, size):
        self.internal = [0] * (size // self.BITS + 1)

    def get(self, index):
        return (self.internal[index // self.BITS] >> (index % self.BITS)) & 1 == 1

    def set_true(self, index):
        self.internal[index // self.BITS] |= 1 << (index % self.BITS)

    def set_internal_or(self, index, element):
        self.internal[index] |= element


def update(dependencies):
    for i in range(len(dependencies)):
        for x in range(len(dependencies)):
            if dependencies[x].get(i):
                for y in range(len(dependencies[0].internal)):
                    dependency_i_y = dependencies[i].internal[y]
                    dependencies[x].set_internal_or(y, dependency_i_y)


def topological_sort(current, dependencies, used, sorted_list):
    used.add(current)
    for i in range(len(dependencies)):
        if i not in used and dependencies[current].get(i):
            topological_sort(i, dependencies, used, sorted_list)
    sorted_list.append(current)


def sort_by_deadlines(deadlines, dependencies, order):
    sorted_set = sorted(((deadline, i) for i, deadline in enumerate(deadlines)), key=lambda x: x[0])

    for u in order:
        new_deadline = deadlines[u]
        for index, (deadline, i) in enumerate(sorted_set):
            if dependencies[u].get(i):
                count = index + 1
                if i != u:
                    new_deadline = min(new_deadline, deadline - (count // 2 + count % 2))

        sorted_set = [x for x in sorted_set if x != (deadlines[u], u)]
        sorted_set.append((new_deadline, u))
        sorted_set.sort(key=lambda x: x[0])

    return sorted_set


def schedule_p2_prec_p1_l_max(deadlines, dependencies):
    update(dependencies)

    used = set()
    topological_sorted = []

    for i in range(len(dependencies)):
        if i not in used and any(dependencies[i].get(j) for j in range(len(dependencies))):
            topological_sort(i, dependencies, used, topological_sorted)

    sorted_deadlines = sort_by_deadlines(deadlines, dependencies, topological_sorted)

    late = float('-inf')
    time = 0
    first_machine = []
    second_machine = []

    waited = [0] * len(dependencies)
    for dep in dependencies:
        for j in range(len(dependencies)):
            if dep.get(j):
                waited[j] += 1

    while sorted_deadlines:
        time += 1

        jobs = [job for job in sorted_deadlines if waited[job[1]] == 0][:2]

        first_machine.append(jobs[0][1] + 1)
        second_machine.append(jobs[1][1] + 1 if len(jobs) > 1 else -1)

        for job in jobs:
            sorted_deadlines.remove(job)
            late = max(late, time - deadlines[job[1]])

            for i in range(len(dependencies)):
                if dependencies[job[1]].get(i):
                    waited[i] -= 1

    return late, time, first_machine, second_machine


def main():
    # Чтение данных из файла
    with open("p2precp1lmax.in") as file:
        n = int(file.readline().strip())  # Читаем количество деталей
        deadlines = list(map(int, file.readline().strip().split()))  # Читаем дедлайны

        dependencies = []
        for _ in range(n):
            bv = BitVec(n)
            row = list(map(int, file.readline().strip().split()))  # Читаем строку зависимости
            for i, value in enumerate(row):
                if value == 1:
                    bv.set_true(i)
            dependencies.append(bv)

    late, time, first_machine, second_machine = schedule_p2_prec_p1_l_max(deadlines, dependencies)

    # Запись результата в файл
    with open("p2precp1lmax.out", "w") as output:
        output.write(f"{late} {time}\n")
        output.write(" ".join(map(str, first_machine)) + "\n")
        output.write(" ".join(map(str, second_machine)) + "\n")


if __name__ == "__main__":
    main()
