import sys
from time import sleep
from heapq import heappush, heappop, heapify
from collections import defaultdict
from itertools import count,repeat,takewhile
from enum import IntEnum


class Dir(IntEnum):
    N = 0
    E = 1
    S = 2
    W = 3


DIRECTIONS = (Dir.N, Dir.E, Dir.S, Dir.W)


def forward(r):
    x, y, d = r
    if d == Dir.N:
        return x - 1, y, d
    if d == Dir.E:
        return x, y + 1, d
    if d == Dir.S:
        return x + 1, y, d
    if d == Dir.W:
        return x, y - 1, d
    raise ValueError("Invalid direction")


FORWARD_COST = 1
TURN_COST = 1000


def turn_cw(r):
    x, y, d = r
    return x, y, DIRECTIONS[(DIRECTIONS.index(d) + 1) % 4]


def turn_ccw(r):
    x, y, d = r
    return x, y, DIRECTIONS[(DIRECTIONS.index(d) - 1) % 4]


EMPTY = "."
WALL = "#"
TARGET = "E"
REINDEER = "S"


def get_input(fd=None):
    if fd is None:
        return sys.stdin.read()
    with open(fd, "r") as f:
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


def next_states(cost, reindeer, walls):
    fx, fy, fd = forward(reindeer)
    if (fx, fy) not in walls:
        yield cost + FORWARD_COST, (fx, fy, fd)
    yield cost + TURN_COST, turn_cw(reindeer)
    yield cost + TURN_COST, turn_ccw(reindeer)


def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    return total_path[::-1]


H_SCORE = defaultdict(lambda: float("inf"))


def h(state, target):
    """Heuristic function"""
    cost, reindeer = state
    rx, ry, d = reindeer
    return H_SCORE[(rx, ry)]
    # # Manhattan distance to goal
    # cost, reindeer = state
    # rx, ry, d = reindeer
    # tx, ty = target
    # return abs(rx - tx) + abs(ry - ty)


def beams(cell, walls):
    x, y = cell
    # Beam south
    s_beam = list(takewhile(lambda c: c not in walls, zip(count(start=x+1,step=1), repeat(y))))
    # Beam west
    w_beam = list(takewhile(lambda c: c not in walls, zip(repeat(x), count(start=y-1,step=-1))))
    # Beam north
    n_beam = list(takewhile(lambda c: c not in walls, zip(count(start=x-1,step=-1), repeat(y))))
    # Beam east
    e_beam = list(takewhile(lambda c: c not in walls, zip(repeat(x), count(start=y+1,step=1))))
    return (s_beam,w_beam,n_beam,e_beam)



def calc_h_score(target, walls, nonwalls):
    """Precompute distances from each cell to target."""
    H_SCORE[target] = 0
    turn_cost = 0
    beam_centers = {target}
    print("Precomputing H score")
    while beam_centers:
        curr = beam_centers.pop()
        score = H_SCORE[curr] + turn_cost
        for beam in beams(curr,walls):
            if not beam:
                continue
            beam_end = beam[-1]
            beam_end_old_score = H_SCORE[beam_end]
            for inc,cell in enumerate(beam,start=1):
                H_SCORE[cell] = min(H_SCORE[cell], score + inc)
            if beam_end_old_score != H_SCORE[cell]:
                # We updated the score at the beam end, rerun from beam_end
                beam_centers.add(beam_end)
        turn_cost = TURN_COST # All beams which arent the first one need turn cost
    # print(H_SCORE)
    print("Done precomputing H score")


def a_star(start, target, walls, nonwalls):
    print("Starting A* ...")
    openheap = [start]
    came_from = {}
    g_score = defaultdict(lambda: float("inf"))
    g_score[start] = 0
    f_score = defaultdict(lambda: float("inf"))
    f_score[start] = h(start, target)

    closest = float('inf')
    while openheap:
        current = heappop(openheap)
        closest = min(closest,abs(current[1][0]-target[0])+abs(current[1][1]-target[1]))
        print(closest, end='\r')
        ccost, creindeer = current
        if creindeer[0] == target[0] and creindeer[1] == target[1]:
            return ccost, reconstruct_path(came_from, current)
        for neighbor in next_states(*current, walls):
            tentative_g_score = neighbor[0]
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + h(neighbor, target)
                if neighbor not in openheap:
                    heappush(openheap, neighbor)
    raise ValueError("Nothing found!")


def main():
    reindeer, target, walls, nonwalls = parse_input(get_input())
    # Precompute heuristic score
    calc_h_score(target, walls, nonwalls)
    path_cost, path = a_star((0, reindeer), target, walls, nonwalls)

    print(path_cost)


main()
