import numpy as np
from dataclasses import dataclass
from collections import Counter


@dataclass
class Input:
    positions: list[int]


def verify_part1(f):
    print("Verifying", f.__name__, "as solution for part 1")
    assert f(data_small) == part1_small_ref_output
    assert f(data) == part1_ref_output
    return f


def verify_part2(f):
    print("Verifying", f.__name__, "as solution for part 2")
    assert f(data_small) == part2_small_ref_output
    assert f(data) == part2_ref_output
    return f


def read_data(path: str) -> Input:
    with open(path) as fp:
        positions = [int(x) for x in fp.read().split(",")]

    return Input(positions=positions)


data = read_data("./input.txt")
data_small = read_data("./input-small.txt")

part1_small_ref_output = 37
part1_ref_output = 337488

part2_small_ref_output = 168
part2_ref_output = 89647695

# -----------------------------------------------------------------------------

@verify_part1
def part1_solve(data: Input) -> int:
    position_buckets = Counter(data.positions)
    min_fuel = min(sum(abs(p - p0)*count for p, count in position_buckets.items())
                   for p0 in position_buckets)
    print(min_fuel)
    return min_fuel


@verify_part2
def part2_solve(data: Input) -> int:
    position_buckets = Counter(data.positions)

    min_fuel = min(sum(( abs(p-p0)*(1+abs(p-p0))//2 ) * count for p, count in position_buckets.items())
                   for p0 in range(min(position_buckets), max(position_buckets)+1))
    print(min_fuel)
    return min_fuel
