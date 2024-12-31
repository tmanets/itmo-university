from typing import List

class Job:
    def __init__(self, time: int, release: int, index: int, f):
        self.time = time
        self.release = release
        self.index = index
        self.f = f
        self.times = []

class Block:
    def __init__(self, start: int, time: int = 0, jobs: List[Job] = None):
        self.start = start
        self.time = time
        self.jobs = jobs if jobs else []
        self.end = self.start + self.time

    def add(self, job: Job):
        self.jobs.append(job)
        self.time += job.time

def topological_sort(jobs: List[Job], edges: List[List[int]], reverse_edges: List[List[int]]) -> List[Job]:
    def depth_first_search(edges, jobs, current_vertex, result, used):
        if current_vertex in used:
            return
        used.add(current_vertex)

        for neighbor in edges[current_vertex]:
            if neighbor not in used:
                depth_first_search(edges, jobs, neighbor, result, used)

        result.append(jobs[current_vertex])

    result = []
    used = set()

    for i in range(len(jobs)):
        if i not in used and not reverse_edges[i]:
            depth_first_search(edges, jobs, i, result, used)

    return result

def create_blocks(jobs: List[Job]) -> List[Block]:
    blocks = []
    for job in jobs:
        if blocks and blocks[-1].end >= job.release:
            block = blocks[-1]
        else:
            block = Block(job.release)
            blocks.append(block)
        block.add(job)
    return blocks

def decompose(edges, block):
    end = block.end
    used = set()
    minimum_job_index = min(enumerate(block.jobs), key=lambda x: x[1].f(end) if all(y not in used for y in edges[x[1].index]) else float('inf'))[0]
    deleted = block.jobs[minimum_job_index]
    block.jobs.pop(minimum_job_index)
    new_blocks = create_blocks(block.jobs)

    if not new_blocks:
        deleted.times.extend([block.start, block.end])
        return deleted.f(end)
    else:
        if block.start < new_blocks[0].start:
            deleted.times.extend([block.start, new_blocks[0].start])
        for i in range(len(new_blocks) - 1):
            deleted.times.extend([new_blocks[i].end, new_blocks[i+1].start])
        if block.end > new_blocks[-1].end:
            deleted.times.extend([new_blocks[-1].end, block.end])
        return max(deleted.f(end), max(decompose(edges, block) for block in new_blocks))

def schedule1PrecPmtnRFMax(jobs: List[Job], edges: List[List[int]], reverse_edges: List[List[int]]) -> int:
    topological_sorted = topological_sort(jobs, edges, reverse_edges)

    for job in reversed(topological_sorted):
        for neighbor in edges[job.index]:
            jobs[neighbor].release = max(jobs[neighbor].release, job.release + job.time)

    return max(decompose(edges, block) for block in create_blocks(topological_sorted))

def main():
    with open("p1precpmtnrifmax.in") as f:
        n = int(f.readline())
        times = [int(x) for x in f.readline().split()]
        releases = [int(x) for x in f.readline().split()]
        m = int(f.readline())

        edges = [[] for _ in range(n)]
        reverse_edges = [[] for _ in range(n)]

        for _ in range(m):
            from_, to = [int(x) - 1 for x in f.readline().split()]
            edges[from_].append(to)
            reverse_edges[to].append(from_)

        jobs = []
        for i in range(n):
            a, b, c = [int(x) for x in f.readline().split()]
            jobs.append(Job(times[i], releases[i], i, lambda time, a=a, b=b, c=c: a * time * time + b * time + c))

        f_max = schedule1PrecPmtnRFMax(jobs, edges, reverse_edges)

        with open("p1precpmtnrifmax.out", "w") as f:
            f.write(str(f_max) + "\n")

            for job in jobs:
                f.write(str(len(job.times) // 2) + " ")
                for time in job.times:
                    f.write(str(time) + " ")
                f.write("\n")

if __name__ == "__main__":
    main()