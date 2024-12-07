#!/usr/bin/env python3
import sys
import operator
import itertools

IN = sys.stdin.read()


def parse_line(line):
    head, body = line.split(": ", 1)
    return (int(head), tuple(map(int, body.split())))


formulas = tuple(parse_line(lin) for lin in IN.splitlines())

OPERATORS = (operator.mul, operator.add)


def operator_assignments(head, body, operators):
    return itertools.product(operators, repeat=len(body) - 1)


def get_calibration_result(formulas, operators):
    total_calibration_result = 0
    for head, body in formulas:
        for op_combi in operator_assignments(head, body, operators):
            acc = body[0]
            for ix, op in enumerate(op_combi, start=1):
                acc = op(acc, body[ix])
                if acc > head:
                    break
            if acc == head:
                total_calibration_result += head
                break
    return total_calibration_result


# Part 1
print(get_calibration_result(formulas, OPERATORS))


# Part 2
concat = lambda i1, i2: int(str(i1) + str(i2))

new_operators = (*OPERATORS, concat)
print(get_calibration_result(formulas, new_operators))
