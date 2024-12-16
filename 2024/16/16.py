import sys
from collections import defaultdict
from enum import IntEnum
from heapq import heappop, heappush
from itertools import count, repeat, takewhile
from pathlib import Path


class Dir(IntEnum):
    N = 0
    E = 1
    S = 2
    W = 3


DIRECTIONS = (Dir.N, Dir.E, Dir.S, Dir.W)


FORWARD_COST = 1
TURN_COST = 1000


EMPTY = "."
WALL = "#"
TARGET = "E"
REINDEER = "S"


def get_input(fd=None):
    if fd is None:
        return sys.stdin.read()
    with Path(fd).open() as f:
        return f.read()


def parse_input(grid):
    lines = grid.splitlines()
    reindeer = (0, 0, Dir.E)
    walls = []
    nonwalls = []
    target = (0, 0)
    for x, line in enumerate(lines):
        for y, cell in enumerate(line):
            if cell == EMPTY:
                nonwalls.append((x, y))
            elif cell == WALL:
                walls.append((x, y))
            elif cell == TARGET:
                target = (x, y)
                nonwalls.append((x, y))
            elif cell == REINDEER:
                reindeer = (x, y, Dir.E)
                nonwalls.append((x, y))
    return reindeer, target, frozenset(walls), frozenset(nonwalls)


def manhattan_dist(c1, c2):
    return abs(c1[0] - c2[0]) + abs(c1[1] - c2[1])


def next_states(cost, reindeer, walls):
    # Reachable junctions
    x, y, d = reindeer
    for i, beam in enumerate(beams((x, y), walls)):
        bd = Dir(i)
        # for bx,by in filter(lambda c: c in junctions, beam):
        for bx, by in beam:
            inc = FORWARD_COST * manhattan_dist((x, y), (bx, by))
            if bd != d:
                inc += TURN_COST
            yield cost + inc, (bx, by, bd)


def beams(cell, walls):
    x, y = cell
    # Beam north
    n_beam = list(
        takewhile(lambda c: c not in walls, zip(count(start=x - 1, step=-1), repeat(y)))
    )
    # Beam east
    e_beam = list(
        takewhile(lambda c: c not in walls, zip(repeat(x), count(start=y + 1, step=1)))
    )
    # Beam south
    s_beam = list(
        takewhile(lambda c: c not in walls, zip(count(start=x + 1, step=1), repeat(y)))
    )
    # Beam west
    w_beam = list(
        takewhile(lambda c: c not in walls, zip(repeat(x), count(start=y - 1, step=-1)))
    )
    return (s_beam, w_beam, n_beam, e_beam)


def bfs(x, y, d, target, walls):
    best_score = defaultdict(lambda: float("inf"))
    best_score[(x, y, d)] = 0
    prev = defaultdict(list)

    heap = []
    heap.append((0, x, y, d))
    while heap:
        print(len(heap), "remaining                 ", end="\r")
        cost, x, y, d = heappop(heap)
        curr = (x, y, d)
        for ncost, (nx, ny, nd) in next_states(cost, curr, walls):
            neighbor = (nx, ny, nd)
            if ncost == best_score[neighbor]:
                # Equivalent path
                prev[neighbor].append(curr)
            elif ncost < best_score[neighbor]:
                # Better path
                prev[neighbor] = [curr]
                best_score[neighbor] = ncost
                heappush(heap, (ncost, *neighbor))

    print(" " * 50, end="\r")
    total = min([best_score[(*target, d)] for d in DIRECTIONS])
    print(total)
    # Find all nodes on a best path
    on_best_path = {(*target, d)}
    to_expand = {(*target, d) for d in DIRECTIONS if best_score[(*target, d)] == total}
    while to_expand:
        curr = to_expand.pop()
        to_expand |= {i for i in prev[curr] if i not in on_best_path}
        on_best_path.add(curr)

    print(len({(x, y) for (x, y, d) in on_best_path}))


def main():
    reindeer, target, walls, nonwalls = parse_input(get_input())
    bfs(*reindeer, target, walls)


main()
