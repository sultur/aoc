import sys
import math
from collections import defaultdict

IN = sys.stdin.read()
NUM_BLINKS = 75

stones = list(map(int, IN.split()))

stones_after_blinks = defaultdict(lambda: [None for _ in range(NUM_BLINKS)])


def one_step(n: int) -> list[str]:
    if n == 0:
        return [1]
    l = int(math.log10(n))+1
    if l % 2 == 0:
        n1, n2 = divmod(n, pow(10,l//2))
        return [n1, n2]
    return [n * 2024]


def calc_num_stones(stone: int, blinks_left: int) -> int:
    if blinks_left <= 0:
        return 1
    blinks_left -= 1
    result = stones_after_blinks[stone][blinks_left]
    if result is not None:
        return result

    next_stones = one_step(stone)
    num_stones = 0
    # For each of the next stones, how many stones do we end up with after the remaining blinks
    for s in next_stones:
        num_stones += calc_num_stones(s, blinks_left)
    stones_after_blinks[stone][blinks_left] = num_stones
    return num_stones


# Part 1
print(sum(calc_num_stones(s, 25) for s in stones))
# Part 2
print(sum(calc_num_stones(s, NUM_BLINKS) for s in stones))
