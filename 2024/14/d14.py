import sys
import re
from math import prod as product
from itertools import count

IN = sys.stdin.read()
LINE_RE = re.compile(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)")

# Each robot is a 4-tuple, (y,x,dy,dx)
robot_start_pos = []
for line in IN.splitlines():
    m = LINE_RE.match(line)
    robot_start_pos.append(tuple(map(int, m.groups())))

WIDTH = 101
HEIGHT = 103
STEPS = 100

# Part 1
UPPER_LEFT = 0
UPPER_RIGHT = 1
LOWER_LEFT = 2
LOWER_RIGHT = 3


def get_quadrant(y, x):
    assert y != WIDTH // 2 and x != HEIGHT // 2
    match (y <= WIDTH // 2, x <= HEIGHT // 2):
        case (True, True):
            return UPPER_LEFT
        case (False, True):
            return UPPER_RIGHT
        case (True, False):
            return LOWER_LEFT
        case (False, False):
            return LOWER_RIGHT


ignored = 0
robots_in_quadrant = [0, 0, 0, 0]
# Simulate robots and count in which
for robot in robot_start_pos:
    y, x, dy, dx = robot
    for _ in range(STEPS):
        y = (y + dy) % WIDTH
        x = (x + dx) % HEIGHT
    # print(y,x)
    if y == WIDTH // 2 or x == HEIGHT // 2:
        ignored += 1
    else:
        robots_in_quadrant[get_quadrant(y, x)] += 1

print(product(robots_in_quadrant))


# Part 2
start = 7000
end = 10000
def print_robots(robot_positions):
    output = ""
    for y in range(WIDTH):
        for x in range(HEIGHT):
            if any(ry == y and rx == x for (ry, rx) in robot_positions):
                output += "X"
            else:
                output += "."
        output += "\n"
    print(output)

def possibly_tree(robot_positions, step):
    return step in range(start,end)

robot_positions = [[y, x] for (y, x, _, _) in robot_start_pos]
robot_vectors = [(dy, dx) for (_, _, dy, dx) in robot_start_pos]
for step in count(start=1):
    print(step)
    print("-" * (WIDTH + 20))
    # Move all robots one step
    for i, (dy, dx) in enumerate(robot_vectors):
        y, x = robot_positions[i]
        robot_positions[i][0] = (y + dy) % WIDTH
        robot_positions[i][1] = (x + dx) % HEIGHT

    if possibly_tree(robot_positions,step):
        print_robots(robot_positions)
