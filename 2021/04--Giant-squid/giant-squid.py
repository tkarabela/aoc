from dataclasses import dataclass
from typing import Optional
import numpy as np
import numpy.typing as npt


@dataclass
class Board:
    numbers: npt.NDArray[np.int8]
    marked: npt.NDArray[np.bool_]
    score: Optional[int] = None

    @classmethod
    def make_board(cls, arr: list[list[int]]):
        numbers = np.asarray(arr, dtype=np.int8)
        assert numbers.shape == (5, 5)

        return cls(
            numbers=numbers,
            marked=np.zeros_like(numbers, dtype=np.bool_),
        )

    def reset(self):
        self.marked[...] = False
        self.score = None

    def has_bingo(self) -> bool:
        return (np.bitwise_and.reduce(self.marked, axis=0).any() or
                np.bitwise_and.reduce(self.marked, axis=1).any())

    def draw_number(self, x: int) -> Optional[int]:
        self.marked |= self.numbers == x
        if self.score is None and self.has_bingo():
            sum_of_unmarked = np.sum(self.numbers.astype(np.int32) * ~self.marked)
            print(self.numbers)
            print(~self.marked)
            print(sum_of_unmarked)
            self.score = sum_of_unmarked * x
            return self.score

        return None

@dataclass
class Input:
    drawn_numbers: list[int]
    boards: list[Board]


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
    drawn_numbers = []
    boards = []
    rows = []
    with open(path) as fp:
        for lineno, line in enumerate(fp, 1):
            line = line.strip()
            if lineno == 1:
                drawn_numbers = [int(x) for x in line.split(",")]
            else:
                if not line:
                    if rows:
                        boards.append(Board.make_board(rows))
                        rows.clear()
                else:
                    rows.append([int(x) for x in line.split()])

    if rows:
        boards.append(Board.make_board(rows))
        rows.clear()

    return Input(drawn_numbers=drawn_numbers, boards=boards)


data = read_data("./input.txt")
data_small = read_data("./input-small.txt")

part1_small_ref_output = 4512
part1_ref_output = 39902

part2_small_ref_output = 1924
part2_ref_output = 26936

# -----------------------------------------------------------------------------

@verify_part1
def part1_solve(data: Input) -> int:
    for b in data.boards:
        b.reset()

    for x in data.drawn_numbers:
        print("drawing", x)
        for i, b in enumerate(data.boards, 1):
            print("board", i)
            score = b.draw_number(x)
            if score is not None:
                print("WIN", score)
                return score

    assert False, "no winning board"


@verify_part2
def part2_solve(data: Input) -> int:
    for b in data.boards:
        b.reset()

    winning_boards = []
    for x in data.drawn_numbers:
        print("drawing", x)
        for i, b in enumerate(data.boards, 1):
            print("board", i)
            score = b.draw_number(x)
            if score is not None:
                winning_boards.append(b)
                print("board wins", score)

    return winning_boards[-1].score
