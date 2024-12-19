import sys
from pathlib import Path
from itertools import product


def get_input(f="in"):
    if not sys.stdin.isatty():
        inp = sys.stdin.read()
    else:
        inp = Path(f).read_text()

    available, designs = inp.split("\n\n")

    return frozenset(available.strip().split(", ")), tuple(designs.strip().split("\n"))


CACHE = {}


def ways_to_design(avail, design):
    if design in CACHE:
        return CACHE[design]
    possible = 0
    if design in avail:
        possible += 1
    for i in range(1, len(design)):
        if design[:i] in avail:
            last_designs = ways_to_design(avail, design[i:])
            possible += last_designs
    CACHE[design] = possible
    return possible


avail, designs = get_input()
num_designs = tuple(map(lambda x: ways_to_design(avail, x), designs))

print(sum(1 for i in num_designs if i > 0))
print(sum(num_designs))
