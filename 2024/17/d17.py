import sys
import re
from itertools import count
from pathlib import Path

import z3

REG_RE = re.compile(r"Register\s?(.):\s*(\d+)\s*")


def get_input(f="in"):
    if not sys.stdin.isatty():
        inp = sys.stdin.read()
    else:
        inp = Path(f).read_text()
    register_in, program_in = inp.split("\n\n")

    registers = {}
    for line in register_in.splitlines():
        m = REG_RE.match(line)
        if m:
            k, v = m.groups()
            registers[k] = int(v)

    program = tuple(map(int, program_in.strip().split(":", 1)[1].split(",")))
    return registers, program


reg, program = get_input()

ADV = 0
BXL = 1
BST = 2
JNZ = 3
BXC = 4
OUT = 5
BDV = 6
CDV = 7


# Part 1
def simulate(reg, program):
    output = []
    pc = 0
    while pc < len(program):
        next_pc = pc + 2
        op = program[pc]
        lit_operand = program[pc + 1]
        combo_operand = (0, 1, 2, 3, reg["A"], reg["B"], reg["C"])[lit_operand]
        if op == ADV:  # 0
            reg["A"] = reg["A"] // (2**combo_operand)
        elif op == BXL:  # 1
            reg["B"] = reg["B"] ^ lit_operand
        elif op == BST:  # 2
            reg["B"] = combo_operand % 8
        elif op == JNZ and reg["A"] != 0:  # 3
            next_pc = lit_operand
        elif op == BXC:  # 4
            reg["B"] = reg["B"] ^ reg["C"]
        elif op == OUT:  # 5
            output.append(combo_operand % 8)
        elif op == BDV:  # 6
            reg["B"] = reg["A"] // (2**combo_operand)
        elif op == CDV:  # 7
            reg["C"] = reg["A"] // (2**combo_operand)
        pc = next_pc
    return tuple(output)


print(",".join(map(str, simulate(reg, program))))


# Part 2
# Condensed formula:
# ((x%8)^1)^(x // (2**((x%8) ^ 2)))
# or ((x&7)^1)^(x >> (((x&7) ^ 2)))
# Then A divided by 8, repeat
def find_a(program):
    s = z3.Solver()
    constraints = []
    a = z3.BitVec("a", 64)
    curr = a
    for n in program:
        nc = z3.BitVecVal(n, 64)
        constraints.append(nc == (((curr & 7) ^ 1) ^ (curr >> ((curr & 7) ^ 2))) & 7)
        curr = curr >> 3
    s.add(constraints)
    # Return smallest solution we find
    sm = None
    while s.check():
        sol = s.model()[a].as_long()
        if sol == sm:  # Found the smallest solution again, just quit
            break
        if sm is None or sol < sm:
            sm = sol
    return sm


print(find_a(program))
