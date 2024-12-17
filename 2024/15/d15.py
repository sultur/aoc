import sys
from itertools import count, repeat, pairwise

IN = sys.stdin.read()
grid, moves = IN.split("\n\n", 1)

EMPTY = "."
WALL = "#"
BOX = "O"
ROBOT = "@"
robot_pos = grid.find(ROBOT)

grid = [list(line) for line in grid.splitlines()]
N_ROWS = len(grid)
N_COLS = len(grid[0])


def print_grid(grid):
    for row in grid:
        print("".join(row))


robot_pos = divmod(robot_pos, N_ROWS)
x, y = robot_pos[0], robot_pos[1] // 2

UP = "^"
RIGHT = ">"
DOWN = "v"
LEFT = "<"
MOVES = frozenset((UP, RIGHT, DOWN, LEFT))


def trail_to_empty(grid, move, x, y):
    if move == UP:
        beam = zip(count(start=-1, step=-1), repeat(0))
    elif move == RIGHT:
        beam = zip(repeat(0), count(start=1, step=1))
    elif move == DOWN:
        beam = zip(count(start=1, step=1), repeat(0))
    elif move == LEFT:
        beam = zip(repeat(0), count(start=-1, step=-1))

    trail = [(x, y)]
    for dx, dy in beam:
        cx, cy = x + dx, y + dy
        trail.append((cx, cy))
        if grid[cx][cy] == EMPTY:
            # Found an empty spot
            return tuple(trail)
        if grid[cx][cy] == WALL:
            # Hit a wall, do nothing
            return tuple()


def trail_to_swaps(trail):
    return list(pairwise(trail))[::-1]


def make_swaps(grid, trail):
    for (lx, ly), (tx, ty) in trail_to_swaps(trail):
        grid[lx][ly], grid[tx][ty] = grid[tx][ty], grid[lx][ly]


def make_move(grid, move, x, y):
    # The robot can only move in this direction
    # if there is an empty cell before hitting a wall
    if trail := trail_to_empty(grid, move, x, y):
        x, y = trail[1]  # Robot moves one step
        # Found an empty cell in this direction
        # Swap the cells backwards
        make_swaps(grid, trail)
    return x, y


for move in moves:
    if move not in MOVES:
        continue
    x, y = make_move(grid, move, x, y)

# Calculate box
gps_sum = 0
for x in range(N_ROWS):
    for y in range(N_COLS):
        if grid[x][y] == BOX:
            gps_sum += 100 * x + y

print(gps_sum)


# Part 2
grid, moves = IN.split("\n\n", 1)
input_grid = [list(line) for line in grid.splitlines()]
REPLACEMENTS = {EMPTY: "..", WALL: "##", BOX: "[]", ROBOT: "@."}

# Scale up map
grid = [list() for _ in range(N_ROWS)]
for x in range(N_ROWS):
    for y in range(N_COLS):
        grid[x].extend(REPLACEMENTS[input_grid[x][y]])


# Find robot again
x, y = next(
    (row, col)
    for row in range(N_ROWS)
    for col in range(N_COLS)
    if grid[row][col] == ROBOT
)


def trail_is_suffix(long, short):
    return long != short and long[-len(short) :] == short


def expand_trail(grid, move, trail):
    trails = set()
    to_check = {trail}
    while to_check:
        trail = to_check.pop()
        if not trail:
            # Empty trail, a wall blocks us from moving
            return ()
        trails.add(trail)
        for tx, ty in trail[1:-1]:
            if grid[tx][ty] == "[":
                to_check.add(trail_to_empty(grid, move, tx, ty + 1))
            if grid[tx][ty] == "]":
                to_check.add(trail_to_empty(grid, move, tx, ty - 1))
    # Remove redundant trails
    shortest_first = sorted(trails, key=len)
    real_trails = set()
    while shortest_first:
        trail = shortest_first.pop()
        if any(trail_is_suffix(long, trail) for long in real_trails):
            continue
        real_trails.add(trail)
    return real_trails


def make_move2(grid, move, x, y):
    if move in (LEFT, RIGHT):
        # Left/right, same as before
        return make_move(grid, move, x, y)

    robot_trail = trail_to_empty(grid, move, x, y)
    # if move == UP and x==6 and y ==3:
    #     breakpoint()
    if trails := expand_trail(grid, move, robot_trail):
        x, y = robot_trail[1]
        while trails:
            make_swaps(grid, trails.pop())
    return x, y


for i, move in enumerate(moves):
    if move not in MOVES:
        continue
    x, y = make_move2(grid, move, x, y)


# Calculate gps sum
gps_sum = 0
for x, line in enumerate(grid):
    for y, cell in enumerate(line):
        if grid[x][y] == "[":
            gps_sum += 100 * x + y

print(gps_sum)
