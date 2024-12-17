import sys

IN = sys.stdin.read()

grid = [[int(c) for c in line] for line in IN.splitlines()]
N_ROWS = len(grid)
N_COLS = len(grid[0])


def path_continuations(grid, x, y):
    """
    Returns coordinates of grid neighbors
    that contain the cell value grid[x][y]+1.
    """
    curr_val = grid[x][y]
    for x2, y2 in [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]:
        if 0 <= x2 < N_ROWS and 0 <= y2 < N_COLS and grid[x2][y2] == curr_val + 1:
            yield (x2, y2)


def distinct_endpoints(grid, x, y):
    """Return set of distinct endpoints reachable from grid[x][y]."""
    if grid[x][y] == 9:
        return {(x, y)}
    destinations = set()
    for x2, y2 in path_continuations(grid, x, y):
        destinations |= distinct_endpoints(grid, x2, y2)
    return destinations


def distinct_paths(grid, x, y):
    """Return number of distinct paths from grid[x][y]."""
    if grid[x][y] == 9:
        return 1
    paths = 0
    for x2, y2 in path_continuations(grid, x, y):
        paths += distinct_paths(grid, x2, y2)
    return paths


endpoint_count = 0
path_count = 0
for x, line in enumerate(grid):
    for y, cell in enumerate(line):
        if cell == 0:
            endpoint_count += len(distinct_endpoints(grid, x, y))
            path_count += distinct_paths(grid, x, y)


print(endpoint_count)
print(path_count)
