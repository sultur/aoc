from collections.abc import Generator, Iterable
import sys
from typing import NamedTuple
import networkx as nx
from pathlib import Path
from itertools import product, pairwise, groupby, chain

# TODO: Unfinished part 2

Point = tuple[int, int]


def manhattan(a: Point, b: Point):
    return sum(abs(i - j) for i, j in zip(a, b))


KEYPAD_POS = {
    "7": (0, 0),
    "8": (0, 1),
    "9": (0, 2),
    "4": (1, 0),
    "5": (1, 1),
    "6": (1, 2),
    "1": (2, 0),
    "2": (2, 1),
    "3": (2, 2),
    "0": (3, 1),
    "A": (3, 2),
}
DPAD_POS = {
    "^": (0, 1),
    "A": (0, 2),
    "<": (1, 0),
    "v": (1, 1),
    ">": (1, 2),
}
KEYPAD_GRAPH: "nx.Graph[Point]" = nx.Graph()
KEYPAD_GRAPH.add_edges_from(
    [
        (n1, n2)
        for n1, n2 in product(KEYPAD_POS.values(), repeat=2)
        if manhattan(n1, n2) == 1
    ]
)
DPAD_GRAPH: "nx.Graph[Point]" = nx.Graph()
DPAD_GRAPH.add_edges_from(
    [
        (n1, n2)
        for n1, n2 in product(DPAD_POS.values(), repeat=2)
        if manhattan(n1, n2) == 1
    ]
)


def get_input(f: str = "in") -> list[str]:
    if not sys.stdin.isatty():
        inp = sys.stdin.read()
    else:
        inp = Path(f).read_text()

    return inp.splitlines()


def translate_to_dcode(a: Point, b: Point) -> str:
    """Return dcode needed to move from a to b."""
    x1, y1 = a
    if b == (x1 - 1, y1):
        return "^"
    if b == (x1 + 1, y1):
        return "v"
    if b == (x1, y1 - 1):
        return "<"
    if b == (x1, y1 + 1):
        return ">"
    raise ValueError(f"Cannot move from {a} to {b} in single instruction")


def code_to_dcodes(
    dcode: str, char_to_point: dict[str, Point], graph: "nx.Graph[Point]"
) -> str:
    seq = ""
    for l1, l2 in pairwise("A" + dcode):
        curr = char_to_point[l1]
        target = char_to_point[l2]
        moves = (
            translate_to_dcode(a, b)
            for a, b in pairwise(nx.shortest_path(graph, curr, target))
        )
        seq += "".join(moves) + "A"
    return seq


def keycode_to_dcodes(keycode: str) -> str:
    """
    For a given keycode, return the dpad command needed to type it out,
    i.e. "023" -> "<A^A>A"
    """
    return code_to_dcodes(keycode, KEYPAD_POS, KEYPAD_GRAPH)


def dcodes_to_dcodes(dcode: str) -> str:
    return code_to_dcodes(dcode, DPAD_POS, DPAD_GRAPH)


def keycode_to_int(kc: str) -> int:
    return int("".join(filter(str.isdecimal, kc)))


class State(NamedTuple):
    written: str
    r1: Point
    r2: Point
    r3: Point


def retain_fewest_turns(move_seqs: list[list[str]]):
    turns = [len(tuple(groupby(s))) for s in move_seqs]
    min_turns = min(turns)
    for seq, t in zip(move_seqs, turns):
        if t == min_turns:
            yield seq


def code_to_all_dcodes(
    dcode: str,
    char_to_point: dict[str, Point],
    graph: "nx.Graph[Point]",
    opt: bool = False,
) -> Generator[str, None, None]:
    seq_combis = []

    for l1, l2 in pairwise("A" + dcode):
        curr = char_to_point[l1]
        target = char_to_point[l2]
        possible_move_seqs = [
            tuple(translate_to_dcode(a, b) for a, b in pairwise(path))
            for path in nx.all_shortest_paths(graph, curr, target)
        ]
        if opt:
            possible_move_seqs = list(retain_fewest_turns(possible_move_seqs))

        seq_combis.append(possible_move_seqs)
        seq_combis.append(["A"])

    for p in product(*seq_combis):
        yield "".join(chain.from_iterable(p))


def iter_dcodes(
    dcode: Iterable[str],
    char_to_point: dict[str, Point],
    graph: "nx.Graph[Point]",
    opt: bool = False,
) -> Generator[str, None, None]:
    for kc in dcode:
        yield from code_to_all_dcodes(kc, char_to_point, graph, opt)


def opt_for_kc(keycode: str, robots_between: int = 2) -> str:
    print("Processing", keycode)
    processed = 0
    shortest_seq = None
    shortest_seq_len = float("inf")

    first_robot = code_to_all_dcodes(keycode, KEYPAD_POS, KEYPAD_GRAPH, opt=True)

    robots_between -= 1
    curr = first_robot
    for _ in range(robots_between):
        curr = iter_dcodes(curr, DPAD_POS, DPAD_GRAPH, opt=True)
    # robot2_seqs = iter_dcodes(first_robot, DPAD_POS, DPAD_GRAPH, opt=True)

    for kc in curr:
        s1 = dcodes_to_dcodes(kc)
        # last_robot = iter_dcodes(curr, DPAD_POS, DPAD_GRAPH)
        # for s1 in last_robot:
        processed += 1
        if len(s1) < shortest_seq_len:
            shortest_seq = s1
            shortest_seq_len = len(shortest_seq)

    assert shortest_seq
    print("Processed:", processed)
    return shortest_seq


def main():
    keycodes = get_input()
    complexity = 0

    for kc in keycodes:
        dpad_seq = opt_for_kc(kc)
        complexity += len(dpad_seq) * keycode_to_int(kc)
        print(dpad_seq)
        print([(k, len(list(g))) for k, g in groupby(sorted(keycode_to_dcodes(kc)))])
        print(
            [
                (k, len(list(g)))
                for k, g in groupby(sorted(dcodes_to_dcodes(keycode_to_dcodes(kc))))
            ]
        )
        print([(k, len(list(g))) for k, g in groupby(sorted(dpad_seq))])
        print(f"{ len(dpad_seq) } * { keycode_to_int(kc) }")
        print()
    print(complexity)

    # TODO: calculate cost of each move and propagate upwards
    print("*" * 200)
    for i in range(1, 5):
        o = opt_for_kc("0", i)
        print(len(o), o)
        print([(k, len(list(g))) for k, g in groupby(sorted(o))])

    # my_kcs = [
    #     "0",
    #     "02",
    #     "029",
    #     "029A",
    #     "1",
    #     "2",
    #     "3",
    #     "4",
    #     "5",
    #     "6",
    #     "7",
    #     "8",
    #     "9",
    #     "1A",
    #     "2A",
    #     "3A",
    #     "4A",
    #     "5A",
    #     "6A",
    #     "7A",
    #     "8A",
    #     "9A",
    #     "0299",
    #     "0296",
    #     "0293",
    #     "029A",
    # ]
    # for kc in my_kcs:
    #     o = opt_for_kc(kc)
    #     print(kc, len(o), o)


main()
