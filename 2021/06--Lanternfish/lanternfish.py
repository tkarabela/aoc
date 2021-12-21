import numpy as np
from collections import Counter
from dataclasses import dataclass


@dataclass
class Input:
    ages: list[int]


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
        ages = [int(x) for x in fp.read().split(",")]

    return Input(ages=ages)


data = read_data("./input.txt")
data_small = read_data("./input-small.txt")

part1_small_ref_output = 5934
part1_ref_output = 387413

part2_small_ref_output = 26984457539
part2_ref_output = 1738377086345

# -----------------------------------------------------------------------------

@verify_part1
def part1_solve(data: Input) -> int:
    age_buckets = np.zeros((9,), dtype=np.int64)
    next_age_buckets = np.zeros((9,), dtype=np.int64)

    for age in data.ages:
        age_buckets[age] += 1

    for day in range(80):
        print(day, age_buckets.sum(), age_buckets)
        next_age_buckets[:] = 0
        next_age_buckets[0:8] = age_buckets[1:9]
        next_age_buckets[6] += age_buckets[0]
        next_age_buckets[8] += age_buckets[0]
        age_buckets[:] = next_age_buckets

    result = age_buckets.sum()
    print(result)
    return result


@verify_part2
def part2_solve(data: Input) -> int:
    age_buckets = np.zeros((9,), dtype=np.int64)
    next_age_buckets = np.zeros((9,), dtype=np.int64)

    for age in data.ages:
        age_buckets[age] += 1

    for day in range(256):
        print(day, age_buckets.sum(), age_buckets)
        next_age_buckets[:] = 0
        next_age_buckets[0:8] = age_buckets[1:9]
        next_age_buckets[6] += age_buckets[0]
        next_age_buckets[8] += age_buckets[0]
        age_buckets[:] = next_age_buckets

    result = age_buckets.sum()
    print(result)
    return result
