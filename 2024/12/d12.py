import sys
from itertools import count, repeat, takewhile
from collections import deque

IN = sys.stdin.read()
grid = IN.splitlines()
N_ROWS = len(grid)
N_COLS = len(grid[0])


def in_bounds(x, y):
    return x in range(N_ROWS) and y in range(N_COLS)


def neighbors(x, y):
    for nx, ny in ((x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)):
        if in_bounds(nx, ny):
            yield (nx, ny)


mapped = [[False for x in row] for row in grid]


def bfs(x, y):
    mapped[x][y] = True
    plant = grid[x][y]
    garden = [(x, y)]

    queue = deque(neighbors(x, y))
    while len(queue) > 0:
        nx, ny = queue.popleft()
        if grid[nx][ny] == plant and (nx, ny) not in garden:
            garden.append((nx, ny))
            mapped[nx][ny] = True
            queue.extend(neighbors(nx, ny))

    return garden


# Part 1
# Collect the different regions
regions = []
for x in range(N_ROWS):
    for y in range(N_COLS):
        if not mapped[x][y]:
            regions.append(bfs(x, y))

# Calculate cost of fencing off region
fence_cost = 0
for reg in regions:
    area = len(reg)
    edges = area * 4  # (We double count the edges on purpose)
    for x, y in reg:
        # For each cell in region, subtract the number of edges that
        # are adjacent to another cell in the region (this also
        # double-counts & cancels out the double-counting above)
        edges -= sum(1 for neighb in neighbors(x, y) if neighb in reg)
    fence_cost += area * edges
print(fence_cost)


# Part 2
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3


# Directed version of neighbors()
def directed_neighbors(x, y):
    for nx, ny, d in (
        (x - 1, y, UP),
        (x, y + 1, RIGHT),
        (x + 1, y, DOWN),
        (x, y - 1, LEFT),
    ):
        yield (nx, ny, d)


def perpendicular(direction):
    if direction in (UP, DOWN):
        return zip(repeat(0), count(start=1))
    return zip(count(start=1), repeat(0))


def get_sides(region):
    """Returns the neighboring cells of each side of a given region."""
    # Get all adjacent cells of region, along with the direction from
    # neighboring region cells
    region_neighbors = set(
        (x, y, d)
        for cell in region
        for (x, y, d) in directed_neighbors(*cell)
        if (x, y) not in region
    )

    def in_reg_neighb(x):
        return x in region_neighbors

    # Group into sets of cells that have the same direction and are adjacent
    sides = []
    while region_neighbors:
        cx, cy, direc = region_neighbors.pop()
        adjacent = {(cx, cy, direc)}
        adjacent.update(
            takewhile(
                in_reg_neighb,
                ((cx + i1, cy + i2, direc) for (i1, i2) in perpendicular(direc)),
            )
        )
        adjacent.update(
            takewhile(
                in_reg_neighb,
                ((cx - i1, cy - i2, direc) for (i1, i2) in perpendicular(direc)),
            )
        )

        sides.append(adjacent)
        region_neighbors -= adjacent
    return sides


new_fence_cost = 0
for reg in regions:
    new_fence_cost += len(reg) * len(get_sides(reg))
print(new_fence_cost)
