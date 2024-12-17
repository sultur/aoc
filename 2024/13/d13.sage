import sys
import re

IN = sys.stdin.read()

BLOCK_RE = re.compile(
    r"""Button A: X\+(?P<X1>[0-9]+), Y\+(?P<Y1>[0-9]+)
Button B: X\+(?P<X2>[0-9]+), Y\+(?P<Y2>[0-9]+)
Prize: X=(?P<X3>[0-9]+), Y=(?P<Y3>[0-9]+)"""
)

machines = []
for block in IN.split("\n\n"):
    m = BLOCK_RE.match(block)
    a_vec = vector((int(m.group("X1")), int(m.group("Y1"))))
    b_vec = vector((int(m.group("X2")), int(m.group("Y2"))))
    p_vec = vector((int(m.group("X3")), int(m.group("Y3"))))
    machines.append((a_vec, b_vec, p_vec))


COST_VEC = vector((3, 1))


def solve(machine):
    av, bv, pv = machine
    # Create matrix A, then find x such that Ax = pv
    A = matrix([av, bv]).T
    x = A.solve_right(pv)  # Solve for x in Ax = pv
    return COST_VEC * x if all(c.is_integer() for c in x) else 0


# Part 1
print(sum(solve(m) for m in machines))

# Part 2
SCALING_FACTOR = 10000000000000
SCALING_VEC = vector((SCALING_FACTOR, SCALING_FACTOR))


def add_scaling_vec(m):
    av, bv, pv = m
    return av, bv, pv + SCALING_VEC


print(sum(solve(m) for m in map(add_scaling_vec, machines)))
