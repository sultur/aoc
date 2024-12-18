import sys
import networkx as nx
from pathlib import Path


def get_input(f="in"):
    if not sys.stdin.isatty():
        inp = sys.stdin.read()
    else:
        inp = Path(f).read_text()

    corrupted_bytes = []
    for line in inp.splitlines():
        x, y = tuple(map(int, line.split(",")))
        corrupted_bytes.append((x, y))

    return tuple(corrupted_bytes)

# Part 1
def print_graph(graph, n_rows, n_cols, path=None):
    for x in range(n_rows):
        line = ""
        for y in range(n_cols):
            if path and (x, y) in path:
                line += "O"
            else:
                line += graph.nodes[(x, y)]["symbol"]
        print(line)


def graph_after_bytes(fallen_bytes, n_rows, n_cols):
    G = nx.Graph()
    for y in range(n_rows):
        for x in range(n_cols):
            symbol = "." if (x, y) not in fallen_bytes else "#"
            G.add_node((x, y), symbol=symbol)
            curr = (x, y)
            if curr in fallen_bytes:
                # This is a wall, don't add edges
                continue
            # Add edge to east cell
            east = (x, y + 1)
            if y + 1 < n_cols and east not in fallen_bytes:
                G.add_edge(curr, east)
            # Add edge to south cell
            south = (x + 1, y)
            if x + 1 < n_rows and south not in fallen_bytes:
                G.add_edge(curr, south, weight=1)
    return G


def part1(corr, byte_count, nr, nc):
    g = graph_after_bytes(corr[:byte_count], nr, nc)
    path = nx.shortest_path(g, (0, 0), (nr - 1, nc - 1), weight="weight")
    print(len(path) - 1)  # Skip first cell, (0,0)


def binary_search(f, lo, hi):
    mid = lo + (hi - lo) // 2
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        fm = f(mid)
        if fm:
            lo = mid + 1
        else:
            hi = mid - 1
    return hi


def part2(corr, nr, nc):
    def f(byte_count):
        g = graph_after_bytes(corr[:byte_count], nr, nc)
        try:
            path = nx.shortest_path(g, (0, 0), (nr - 1, nc - 1), weight="weight")
            return True
        except:
            return False

    print(corr[binary_search(f, 0, len(corr))])


n_rows = n_cols = 71
byte_count = 1024
corr = get_input()
part1(corr, byte_count, n_rows, n_cols)
part2(corr, n_rows, n_cols)
