import sys
import networkx as nx
from collections import defaultdict
from pathlib import Path


def get_input(f="in"):
    if not sys.stdin.isatty():
        inp = sys.stdin.read()
    else:
        inp = Path(f).read_text()

    start = (0, 0)
    end = (0, 0)
    nonwalls = []
    for row, line in enumerate(inp.splitlines()):
        for col, cell in enumerate(line):
            curr = (row, col)
            if cell == "#":
                continue
            nonwalls.append(curr)
            if cell == "S":
                start = curr
            elif cell == "E":
                end = curr

    return start, end, frozenset(nonwalls)


def neighbors(cell):
    x, y = cell
    return ((x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1))


def mh_dist(x, y, x2, y2):
    """Manhattan distance"""
    return abs(x - x2) + abs(y - y2)


def surroundings(cell, d):
    """Return all cells that have manhattan distance d or less from cell."""
    x, y = cell
    for x2 in range(x - d, x + d + 1):
        for y2 in range(y - d, y + d + 1):
            mhd = mh_dist(x, y, x2, y2)
            if mhd <= d:
                yield (x2, y2)


def create_graph(nonwalls):
    """Create nx graph."""
    g = nx.Graph()
    for cell in nonwalls:
        for ncell in neighbors(cell):
            if ncell in nonwalls:
                g.add_edge(cell, ncell)
    return g


def solve_with_cheat(s, e, nonwalls, g, cheat_length, moves_to_save):
    shortest = nx.shortest_path(g, s, e)
    baseline = len(shortest)
    dist = {}
    for i, cell in enumerate(shortest):
        dist[cell] = (i, baseline - i)

    assert not any(x not in dist for x in nonwalls), "Non-wall found not on path S->E"

    def possible_cheats(cell):
        cell_to_e = dist[cell][1]
        pos_cheats = set()
        # Return all those non-wall cells at distance <=cheat_length from cell
        for cell2 in surroundings(cell, cheat_length):
            if cell2 not in nonwalls:
                # End up in wall, not valid cheat
                continue
            if cell_to_e - dist[cell2][1] <= moves_to_save:
                # Not enough of a shortcut
                continue
            pos_cheats.add((cell, cell2))
        return pos_cheats

    cheats = defaultdict(set)
    for cell in nonwalls:
        if cell == e:
            continue
        for cheat in possible_cheats(cell):
            new_path_len = (
                dist[cell][0] + mh_dist(*cheat[0], *cheat[1]) + dist[cheat[-1]][1]
            )
            saves = baseline - new_path_len
            if saves >= moves_to_save:
                cheats[saves].add(cheat)
    return cheats


start, end, nonwalls = get_input()
g = create_graph(nonwalls)
cheats = solve_with_cheat(start, end, nonwalls, g, cheat_length=2, moves_to_save=100)
print("Part 1:", sum(len(v) for k, v in cheats.items()))

cheats = solve_with_cheat(start, end, nonwalls, g, cheat_length=20, moves_to_save=100)
print("Part 2:", sum(len(v) for k, v in cheats.items()))
