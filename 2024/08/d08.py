import sys
from math import gcd
from collections import defaultdict
from itertools import combinations, chain, count, takewhile

IN = sys.stdin.read()
EMPTY = "."

# Maps each frequency to list of antenna positions
antennas = defaultdict(list)
grid = IN.splitlines()

N_ROWS = len(grid)
N_COLS = len(grid[0])

for x, line in enumerate(grid):
    for y, char in enumerate(line):
        if char != EMPTY:
            antennas[char].append((x, y))


def legal_pos(pos):
    return 0 <= pos[0] < N_ROWS and 0 <= pos[1] < N_COLS


# Part 1
def antinodes_for_freq(positions):
    antinodes = set()
    for pair in combinations(positions, 2):
        ((x1, y1), (x2, y2)) = pair
        # Calculate the step size: (x1,y1) -> (x2,y2)
        dx, dy = (x2 - x1, y2 - y1)
        cand1 = (x2 + dx, y2 + dy)
        cand2 = (x1 - dx, y1 - dy)
        for node in filter(legal_pos, (cand1, cand2)):
            antinodes.add(node)
    return antinodes


antinodes = set(
    node for positions in antennas.values() for node in antinodes_for_freq(positions)
)
print(len(antinodes))


# Part 2
def antinodes_for_freq2(positions):
    antinodes = set()
    for pair in combinations(positions, 2):
        ((x1, y1), (x2, y2)) = pair
        # Calculate the step size: (x1,y1) -> (x2,y2)
        dx, dy = (x2 - x1, y2 - y1)
        # Get smallest integer step size
        divisor = gcd(dx, dy)
        dx, dy = dx // divisor, dy // divisor
        # Create a beam in each direction generating antinode coordinates
        beam1 = takewhile(
            legal_pos, ((x1 + i * dx, y1 + i * dy) for i in count(start=0, step=1))
        )
        beam2 = takewhile(
            legal_pos, ((x1 + i * dx, y1 + i * dy) for i in count(start=-1, step=-1))
        )
        for node in chain(beam1, beam2):
            antinodes.add(node)
    return antinodes


antinodes = set(
    node for positions in antennas.values() for node in antinodes_for_freq2(positions)
)
print(len(antinodes))
