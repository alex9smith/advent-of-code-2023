from typing import List
from dataclasses import dataclass
from string import ascii_lowercase

REPLACE_DIGITS = {
    "one": "o1e",
    "two": "t2o",
    "three": "t3e",
    "four": "f4r",
    "five": "f5e",
    "six": "s6x",
    "seven": "s7n",
    "eight": "e8t",
    "nine": "n9e",
}

REMOVE_LETTERS = {ord(i): None for i in ascii_lowercase}

type Line = str
type Digit = str
type CalibrationValue = int


@dataclass
class SearchResult:
    found: bool
    digit: Digit


def search_for_first_spelled_digit(line: Line) -> SearchResult:
    locations = {}
    for digit in REPLACE_DIGITS.keys():
        location = line.find(digit)
        if location != -1:
            locations[digit] = location

    if len(locations) == 0:
        return SearchResult(False, "")

    return SearchResult(True, min(locations.items(), key=lambda l: l[1])[0])


def replace_spelled_with_digits(line: Line) -> Line:
    found = True
    new_line = line
    while found:
        result = search_for_first_spelled_digit(new_line)
        if result.found:
            new_line = new_line.replace(result.digit, REPLACE_DIGITS[result.digit])

        found = result.found

    return new_line


def remove_letters(line: Line) -> Line:
    return line.translate(REMOVE_LETTERS)


def get_first_last(line: Line) -> CalibrationValue:
    return int(line[0] + line[-1])


def sum_calibration_values(values: List[Line]) -> int:
    return sum(get_first_last(remove_letters(v)) for v in values)


if __name__ == "__main__":
    with open("./advent_of_code/day_01/day_01.txt", "r") as file:
        calibration_lines = [line.strip() for line in file.readlines()]

    print("part 1")
    print(sum_calibration_values(calibration_lines))

    print("part 2")
    print(
        sum_calibration_values(
            [replace_spelled_with_digits(l) for l in calibration_lines]
        )
    )
