from typing import List, TypeVar
from dataclasses import dataclass

T = TypeVar("T")
type Schematic = List[str]


@dataclass
class ParseResult:
    line_length: int
    schematic: Schematic


@dataclass
class NumberPosition:
    start: int
    end: int
    number: int


def parse(raw: str) -> ParseResult:
    lines = [line.replace("\n", "").strip() for line in raw.split("\n")]
    return ParseResult(
        schematic=[p for line in lines if line != "" for p in line],
        line_length=len(lines[0]),
    )


def safe_get_from_list(list: List[T], index: int) -> T | None:
    if index < 0:
        return None
    try:
        return list[index]
    except IndexError:
        return None


def not_number_or_period(check: str) -> bool:
    return not (check.isnumeric() or check == ".")


def number_next_to_symbol(
    schematic: Schematic, position: NumberPosition, line_length: int
) -> bool:
    above = [
        i
        for i in range(position.start - 1 - line_length, position.end + 2 - line_length)
    ]
    below = [
        i
        for i in range(position.start - 1 + line_length, position.end + 2 + line_length)
    ]
    positions = (
        [
            position.start - 1,
            position.end + 1,
        ]
        + above
        + below
    )

    adjacent_items = [safe_get_from_list(schematic, position) for position in positions]
    return any(not_number_or_period(item) for item in adjacent_items if item)


def find_number_in_schematic(schematic: Schematic, start: int) -> NumberPosition | None:
    index = start
    continue_search = True
    in_number = False
    number_parts = []
    number_start = 0
    number_end = 0

    while (index < len(schematic)) & continue_search:
        item = schematic[index]
        if item.isnumeric():
            if not in_number:
                number_start = index
                in_number = True

            number_parts.append(item)

        elif in_number:
            number_end = index - 1
            continue_search = False

        index = index + 1

    if in_number:
        return NumberPosition(
            number_start, number_end, number=int("".join(number_parts))
        )

    else:
        return None


def sum_engine_part_numbers(schematic: ParseResult) -> int:
    part_sum = 0
    index = 0
    continue_search = True

    while continue_search:
        position = find_number_in_schematic(schematic.schematic, index)
        if position is not None:
            if number_next_to_symbol(
                schematic.schematic, position, schematic.line_length
            ):
                part_sum += position.number

            index = position.end + 1

        else:
            continue_search = False
            index += 1

    return part_sum


if __name__ == "__main__":
    with open("./advent_of_code/day_03/day_03.txt", "r") as file:
        raw = file.read()

    parsed = parse(raw)

    print("part 1")
    print(sum_engine_part_numbers(parsed))
