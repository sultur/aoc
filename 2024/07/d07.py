#!/usr/bin/env python3
import sys
import operator
from functools import partial

IN = sys.stdin.read()


def parse_line(line):
    head, body = line.split(": ", 1)
    return (int(head), tuple(map(int, body.split())))


formulas = tuple(parse_line(lin) for lin in IN.splitlines())
ops = (operator.mul, operator.add)


def get_calibration_result(formulas, ops):
    total_calibration_result = 0
    for head, body in formulas:
        less_than_head = partial(operator.ge, head)
        results = [body[0]]
        for n in body[1:]:
            results = list(
                filter(less_than_head, (op(x, n) for x in results for op in ops))
            )
        if head in results:
            total_calibration_result += head
    return total_calibration_result


# Part 1
print(get_calibration_result(formulas, ops))


# Part 2
def concat(a, b):
    return int(str(a) + str(b))


ops = (*ops, concat)
print(get_calibration_result(formulas, ops))
