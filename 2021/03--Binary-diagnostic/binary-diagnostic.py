from dataclasses import dataclass
import numpy as np
import numpy.typing as npt
import scipy.stats


@dataclass
class Input:
    matrix: npt.NDArray[np.bool_]


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
    rows = []
    with open(path) as fp:
        for line in fp:
            line = line.strip()
            if line:
                digits = [int(x) for x in line]
                rows.append(digits)
    return Input(matrix=np.asarray(rows, dtype=np.bool_))


data = read_data("./input.txt")
data_small = read_data("./input-small.txt")

part1_small_ref_output = 198
part1_ref_output = 2967914

part2_small_ref_output = 230
part2_ref_output = 7041258

# -----------------------------------------------------------------------------

def binvec_to_int(v: npt.NDArray[np.bool_]) -> int:
    x = 0
    for digit in v:
        x <<= 1
        x += int(digit)
    return x


@verify_part1
def part1_solve(data: Input) -> int:
    A = data.matrix

    gamma_rate_vec: np.ndarray = scipy.stats.mode(A, axis=0).mode[0]
    epsilon_rate_vec = ~gamma_rate_vec

    gamma_rate = binvec_to_int(gamma_rate_vec)
    epsilon_rate = binvec_to_int(epsilon_rate_vec)

    return gamma_rate * epsilon_rate


@verify_part2
def part2_solve(data: Input) -> int:
    A = data.matrix
    num_rows, num_cols = A.shape

    oxygen_row_mask = np.ones_like(A[:,0], dtype=np.bool_)
    co2_row_mask = np.ones_like(A[:,0], dtype=np.bool_)
    oxygen_rating = None
    co2_rating = None

    for i in range(num_cols):
        print("i", i)
        if oxygen_rating is not None and co2_rating is not None:
            break

        col = A[:,i]
        num_ones_oxygen = np.count_nonzero(col & oxygen_row_mask)
        num_zeros_oxygen = np.count_nonzero(~col & oxygen_row_mask)
        num_ones_co2 = np.count_nonzero(col & co2_row_mask)
        num_zeros_co2 = np.count_nonzero(~col & co2_row_mask)

        value_oxygen = 1 if num_ones_oxygen >= num_zeros_oxygen else 0
        value_co2 = 0 if num_ones_co2 >= num_zeros_co2 else 1

        oxygen_row_mask &= col == value_oxygen
        co2_row_mask &= col == value_co2
        print("value oxygen", value_oxygen, "value co2", value_co2)

        if oxygen_rating is None and np.count_nonzero(oxygen_row_mask) == 1:
            oxygen_rating = binvec_to_int(A[np.argmax(oxygen_row_mask)])
            print("oxygen", oxygen_rating)
        if co2_rating is None and np.count_nonzero(co2_row_mask) == 1:
            co2_rating = binvec_to_int(A[np.argmax(co2_row_mask)])
            print("co2", co2_rating)

    print(oxygen_rating, co2_rating)
    return oxygen_rating * co2_rating
