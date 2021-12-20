import re
from collections import Counter
from dataclasses import dataclass


@dataclass
class Segment:
    start: tuple[int, int]
    end: tuple[int, int]

    def is_horizontal_vertical(self) -> bool:
        return (self.start[0] == self.end[0] or
                self.start[1] == self.end[1])

    def iter_points(self):
        if self.start == self.end:
            yield self.start
            return

        dx, dy = [b-a for a, b in zip(self.start, self.end)]
        if dx != 0:
            dx /= abs(dx)
        if dy != 0:
            dy /= abs(dy)

        x, y = self.start
        yield x, y
        while True:
            x, y = x+dx, y+dy
            yield x, y
            if (x, y) == self.end:
                break

@dataclass
class Input:
    segments: list[Segment]


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
    segments = []
    with open(path) as fp:
        for lineno, line in enumerate(fp, 1):
            if m := re.match(r"(\d+),(\d+) -> (\d+),(\d+)", line):
                x1, y1, x2, y2 = map(int, m.groups())
                segments.append(Segment(start=(x1, y1), end=(x2, y2)))

    return Input(segments=segments)


data = read_data("./input.txt")
data_small = read_data("./input-small.txt")

part1_small_ref_output = 5
part1_ref_output = 8111

part2_small_ref_output = 12
part2_ref_output = 22088

# -----------------------------------------------------------------------------

@verify_part1
def part1_solve(data: Input) -> int:
    c = Counter()

    for s in data.segments:
        if s.is_horizontal_vertical():
            c.update(s.iter_points())

    output = 0

    for _, count in c.items():
        if count >= 2:
            output += 1

    return output


@verify_part2
def part2_solve(data: Input) -> int:
    c = Counter()

    for s in data.segments:
        c.update(s.iter_points())

    output = 0

    for _, count in c.items():
        if count >= 2:
            output += 1

    return output
