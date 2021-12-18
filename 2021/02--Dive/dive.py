from dataclasses import dataclass


@dataclass
class Input:
    commands: list[tuple[str, int]]


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
    output = []
    with open(path) as fp:
        for line in fp:
            line = line.strip()
            if line:
                command, value = line.split()
                output.append((command, int(value)))
    return Input(commands=output)


data = read_data("./input.txt")
data_small = read_data("./input-small.txt")

part1_small_ref_output = 150
part1_ref_output = 1762050

part2_small_ref_output = 900
part2_ref_output = 1855892637

# -----------------------------------------------------------------------------

@verify_part1
def part1_solve(data: Input) -> int:
    position, depth = 0, 0
    for command, value in data.commands:
        match command:
            case "forward":
                position += value
            case "down":
                depth += value
            case "up":
                depth -= value

    return position * depth


@verify_part2
def part2_solve(data: Input) -> int:
    position, depth, aim = 0, 0, 0
    for command, value in data.commands:
        match command:
            case "forward":
                position += value
                depth += aim * value
            case "down":
                aim += value
            case "up":
                aim -= value

    return position * depth
