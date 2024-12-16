import sys
from time import sleep
from heapq import heappush, heappop, heapify
from collections import defaultdict
from itertools import count, repeat, takewhile
from enum import IntEnum


class Dir(IntEnum):
    N = 0
    E = 1
    S = 2
    W = 3


DIRECTIONS = (Dir.N, Dir.E, Dir.S, Dir.W)


def beam_forward(r, walls):
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


def get_junctions(reindeer, target, walls, nonwalls):
    junctions = {reindeer[:2], target}
    for cell in nonwalls:
        for beam in beams(cell, walls):
            if beam:
                # Add last cell in every beam as a junction
                junctions.add(beam[-1])
    return junctions

def manhattan_dist(c1,c2):
    return abs(c1[0]-c2[0]) + abs(c1[1]-c2[1])

def next_states(cost, reindeer, junctions, walls):
    # Reachable junctions
    x,y,d = reindeer
    for i,beam in enumerate(beams((x,y), walls)):
        bd = Dir(i)
        # for bx,by in filter(lambda c: c in junctions, beam):
        for bx,by in beam:
            inc = FORWARD_COST * manhattan_dist((x,y), (bx,by))
            if bd != d:
                inc += TURN_COST
            yield cost+inc, (bx,by, bd)
        
    # d = reindeer[-1]
    # beam = beams(reindeer[:2], walls)[d.value]
    # for i,cell in enumerate(beam,start=1):
    #     # if cell in junctions:
    #     yield cost + FORWARD_COST*i, (*cell, d)
    # yield cost + TURN_COST, turn_cw(reindeer)
    # yield cost + TURN_COST, turn_ccw(reindeer)


def reconstruct_paths(came_from, current):
    total_path = set()
    to_expand = {current}
    while to_expand:
        current = to_expand.pop()
        for predecessor in came_from[current]:
            x,y,d = predecessor
            if (x,y) not in total_path:
                to_expand.add(predecessor)
            total_path.add((x,y))
    return total_path


H_SCORE = defaultdict(lambda: float("inf"))


def h(state, target):
    """Heuristic function"""
    # cost, reindeer = state
    # rx, ry, d = reindeer
    # return H_SCORE[(rx, ry)]
    # Manhattan distance to goal
    reindeer = state
    rx, ry, d = reindeer
    tx, ty = target
    return abs(rx - tx) + abs(ry - ty)


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


def calc_h_score(target, walls, nonwalls):
    """Precompute distances from each cell to target."""
    H_SCORE[target] = 0
    turn_cost = 0
    beam_centers = {target}
    print("Precomputing H score")
    while beam_centers:
        curr = beam_centers.pop()
        score = H_SCORE[curr] + turn_cost
        for beam in beams(curr, walls):
            if not beam:
                continue
            beam_end = beam[-1]
            beam_end_old_score = H_SCORE[beam_end]
            for inc, cell in enumerate(beam, start=1):
                H_SCORE[cell] = min(H_SCORE[cell], score + inc)
            if beam_end_old_score != H_SCORE[cell]:
                # We updated the score at the beam end, rerun from beam_end
                beam_centers.add(beam_end)
        turn_cost = TURN_COST  # All beams which arent the first one need turn cost
    # print(H_SCORE)
    print("Done precomputing H score")


def a_star(x,y,d, target, junctions, walls, nonwalls):
    print("Starting A* ...")
    came_from = defaultdict(list)
    g_score = defaultdict(lambda: float("inf"))
    g_score[(x,y)] = 0
    f_score = defaultdict(lambda: float("inf"))
    fsc = h((x,y,d), target)
    f_score[(x,y)] = fsc
    openheap = [(fsc,x,y,d)]

    closest = float("inf")
    while openheap:
        fsc, x,y,d = heappop(openheap)
        # print(x,y,d)
        closest = min(closest, manhattan_dist((x,y), target))
        print(closest,len(openheap), "remaining", end="\r")
        ccost = g_score[(x,y)]
        # if (x,y) == target:
        #     return ccost, reconstruct_paths(came_from, (x,y,d))
        for ncost, (nx,ny,nd) in next_states(ccost, (x,y,d), junctions, walls):
            tentative_g_score = ncost
            if tentative_g_score == g_score[(nx,ny)]:
                came_from[(nx,ny,nd)].append((x,y,d))
            if tentative_g_score < g_score[(nx,ny)]:
                came_from[(nx,ny,nd)] = [(x,y,d)]
                g_score[(nx,ny)] = tentative_g_score
                nfsc = tentative_g_score + h((nx,ny,nd), target)
                f_score[(nx,ny)] = nfsc
                neighb = (nfsc, nx,ny,nd)
                if neighb not in openheap:
                    heappush(openheap, neighb)

    return ccost,reconstruct_paths(came_from, target)


def main():
    reindeer, target, walls, nonwalls = parse_input(get_input())
    junctions = get_junctions(reindeer, target, walls, nonwalls)
    # Precompute heuristic score
    calc_h_score(target, walls, nonwalls)
    path_cost, path = a_star(*reindeer, target, junctions, walls, nonwalls)

    print()
    print(path_cost)
    print(len(path))


main()
