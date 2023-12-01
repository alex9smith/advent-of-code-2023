from typing import List
from string import ascii_lowercase

REMOVE_LETTERS = {ord(i): None for i in ascii_lowercase}

type Line = str
type CalibrationValue = int


def remove_letters(line: Line) -> Line:
    return line.translate(REMOVE_LETTERS)


def get_first_last(line: Line) -> CalibrationValue:
    return int(line[0] + line[-1])


def sum_calibration_values(values: List[Line]) -> int:
    return sum(get_first_last(remove_letters(v)) for v in values)


if __name__ == "__main__":
    with open("./advent_of_code/day_01/day_01.txt", "r") as file:
        calibration_lines = [line.strip() for line in file.readlines()]

    print(sum_calibration_values(calibration_lines))
