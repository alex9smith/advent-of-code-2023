from day_03 import (
    parse,
    safe_get_from_list,
    not_number_or_period,
    number_next_to_symbol,
    find_number_in_schematic,
    sum_engine_part_numbers,
    NumberPosition,
)

PART_1_RAW = """467..114..\n
...*......\n
..35..633.\n
......#...\n
617*......\n
.....+.58.\n
..592.....\n
......755.\n
...$.*....\n
.664.598.."""


def test_parse():
    parsed = parse(PART_1_RAW)
    assert parsed.line_length == 10
    assert parsed.schematic[0:11] == [
        "4",
        "6",
        "7",
        ".",
        ".",
        "1",
        "1",
        "4",
        ".",
        ".",
        ".",
    ]


def test_safe_get_from_list():
    LIST = [i for i in range(10)]
    assert safe_get_from_list(LIST, 0) == 0
    assert safe_get_from_list(LIST, 5) == 5
    assert safe_get_from_list(LIST, 20) == None
    assert safe_get_from_list(LIST, -1) == None


def test_not_number_or_period():
    assert not not_number_or_period(".")
    assert not not_number_or_period("5")
    assert not_number_or_period("a")
    assert not_number_or_period("+")


def test_number_next_to_symbol():
    parsed = parse(PART_1_RAW)

    assert number_next_to_symbol(
        parsed.schematic, NumberPosition(0, 2, 1), parsed.line_length
    )
    assert not number_next_to_symbol(
        parsed.schematic, NumberPosition(5, 7, 1), parsed.line_length
    )


def test_find_number_in_schematic():
    parsed = parse(PART_1_RAW)
    result = find_number_in_schematic(parsed.schematic, 0)
    assert result is not None
    assert result.start == 0
    assert result.end == 2
    assert result.number == 467

    result = find_number_in_schematic(parsed.schematic, 99)
    assert result is None


def test_sum_engine_part_numbers():
    parsed = parse(PART_1_RAW)
    assert sum_engine_part_numbers(parsed) == 4361
