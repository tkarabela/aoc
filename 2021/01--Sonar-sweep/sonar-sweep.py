import numpy as np
from swiplserver import PrologMQI


def part1_solve_numpy(data: list[int]) -> int:
    return np.sum(np.diff(data) > 0)


def part1_solve_prolog(data: list[int]) -> int:
    with PrologMQI() as mqi:
        with mqi.create_thread() as prolog_thread:
            prolog_thread.query("['./sonar-sweep.pl'].")
            results = prolog_thread.query(f"foo({data!r}, X).")
            assert len(results) == 1
            result = results[0]["X"]
            return result


def part2_solve_numpy(data: list[int]) -> int:
    data = np.asarray(data, dtype=int)
    return np.sum((data[3:] - data[:-3]) > 0)


def part2_solve_comprehension(a: list[int]) -> int:
    # a1 + a2 + a3 < a2 + a3 + a4  <==>  a1 < a4

    n = len(a)
    return sum(a[i] < a[i+3] for i in range(n-3))


def part2_solve_iterative(a: list[int]) -> int:
    count = 0

    for i in range(len(a)-3):
        if sum(a[i:i+3]) < sum(a[i+1:i+4]):
            count += 1

    return count


def part2_solve_prolog(data: list[int]) -> int:
    with PrologMQI() as mqi:
        with mqi.create_thread() as prolog_thread:
            prolog_thread.query("['./sonar-sweep.pl'].")
            results = prolog_thread.query(f"bar({data!r}, Temp), foo(Temp, X).")
            assert len(results) == 1
            result = results[0]["X"]
            return result

# -----------------------------------------------------------------------------

def read_data(path: str) -> list[int]:
    output = []
    with open(path) as fp:
        for line in fp:
            line = line.strip()
            if line:
                output.append(int(line))
    return output


data = read_data("./input.txt")
data_small = read_data("./input-small.txt")

part1_small_ref_output = 7
part1_ref_output = 1482

part2_small_ref_output = 5
part2_ref_output = 1518


def verify_part1(f):
    print("Verifying", f.__name__, "as solution for part 1")
    assert f(data_small) == part1_small_ref_output
    assert f(data) == part1_ref_output


def verify_part2(f):
    print("Verifying", f.__name__, "as solution for part 2")
    assert f(data_small) == part2_small_ref_output
    assert f(data) == part2_ref_output

# -----------------------------------------------------------------------------

verify_part1(part1_solve_numpy)
verify_part1(part1_solve_prolog)
verify_part2(part2_solve_numpy)
verify_part2(part2_solve_comprehension)
verify_part2(part2_solve_iterative)
verify_part2(part2_solve_prolog)
