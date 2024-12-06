import sys

IN = sys.stdin.read()

OBSTACLE = "#"
GUARD_SYMBOLS = "^>v<"  # Directions the guard can face, N,E,S,W (ORDER MATTERS!)

# Directions
NORTH = "^"
EAST = ">"
SOUTH = "v"
WEST = "<"

CHANGE_IN_POS = {NORTH: (-1, 0), EAST: (0, 1), SOUTH: (1, 0), WEST: (0, -1)}

MAP = IN.splitlines()

MAX_ROW = len(MAP) - 1
MAX_COL = len(MAP[0]) - 1

# (row, col) coordinates for each obstacle, upper left corner is (0,0)
OBSTACLES = frozenset(
    [
        (row, col)
        for row, line in enumerate(MAP)
        for col, cell in enumerate(line)
        if cell == OBSTACLE
    ]
)

# Coordinates of where the guard starts
curr_row, curr_col = next(
    (row, col)
    for row, line in enumerate(MAP)
    for col, cell in enumerate(line)
    if cell in GUARD_SYMBOLS
)
curr_direction = MAP[curr_row][curr_col]

is_in_bounds = lambda row, col: 0 <= row <= MAX_ROW and 0 <= col <= MAX_COL
is_legal_pos = lambda row, col: is_in_bounds(row, col) and (row, col) not in OBSTACLES
turn_clockwise = lambda curr: GUARD_SYMBOLS[
    (GUARD_SYMBOLS.index(curr) + 1) % len(GUARD_SYMBOLS)
]


def next_pos(row, col, direction):
    change_row, change_col = CHANGE_IN_POS[direction]
    return (row + change_row, col + change_col)


def guard_trail(row, col, direction):
    yield (row, col)
    while True:
        # Calculate next coordinate
        next_row, next_col = next_pos(row, col, direction)
        if not is_in_bounds(next_row, next_col):
            # Guard leaves the map
            break
        if (next_row, next_col) in OBSTACLES:
            # Guard hits an obstacle and turns right/clockwise
            direction = turn_clockwise(direction)
            continue
        row, col = next_row, next_col
        yield (row, col)


# Part 1
print(len(set(guard_trail(curr_row, curr_col, curr_direction))))
# (The set is inefficient)

# Part 2
