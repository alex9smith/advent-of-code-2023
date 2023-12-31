from typing import List
from pytest import fixture
from day_03 import (
    Schematic,
    Position,
    is_not_numeric_or_period,
    sum_part_numbers,
    sum_gear_ratios,
)

PART_1_RAW = [
    "467..114..",
    "...*......",
    "..35..633.",
    "......#...",
    "617*......",
    ".....+.58.",
    "..592.....",
    "......755.",
    "...$.*....",
    ".664.598..",
]


class TestPosition:
    def test_contains(self):
        base = Position(1, 1, 5)

        test_cases = [
            (Position(1, 2, 3), True),
            (Position(1, 2, 6), False),
            (Position(2, 2, 3), False),
            (Position(1, 0, 3), False),
        ]

        for case in test_cases:
            assert base.contains(case[0]) == case[1]


class TestSchematic:
    @fixture
    def schematic(self) -> Schematic:
        return Schematic.parse([line.strip() for line in PART_1_RAW])

    @fixture
    def numbers(self, schematic: Schematic) -> List[Position]:
        return schematic.find_all_numbers()

    def test_parse(self, schematic):
        assert schematic.rows == 10
        assert schematic.columns == 10

    def test_find_all_numbers(self, numbers: List[Position]):
        assert numbers[0] == Position(0, 0, 2)
        assert numbers[-1] == Position(9, 5, 7)

    def test_get_valid_values_for_position(
        self, schematic: Schematic, numbers: List[Position]
    ):
        assert schematic.get_valid_values_for_position(numbers[0]) == "467"
        assert schematic.get_valid_values_for_position(numbers[1]) == "114"
        assert schematic.get_valid_values_for_position(numbers[-1]) == "598"

        assert schematic.get_valid_values_for_position(Position(0, -1, 2)) == "467"
        assert schematic.get_valid_values_for_position(Position(0, 5, 200)) == "114.."

        assert schematic.get_valid_values_for_position(Position(-1, 0, 2)) == ""
        assert (
            schematic.get_valid_values_for_position(Position(schematic.rows + 1, 0, 2))
            == ""
        )

    def test_is_position_part_number(
        self, schematic: Schematic, numbers: List[Position]
    ):
        assert schematic.is_position_part_number(numbers[-1])
        assert not schematic.is_position_part_number(numbers[1])
        assert schematic.is_position_part_number(numbers[0])

    def test_find_all_gears(self, schematic: Schematic):
        gears = schematic.find_all_gears()
        assert len(gears) == 3
        assert gears[0] == Position(1, 3, 3)


def test_is_not_numeric_or_period():
    assert not is_not_numeric_or_period(".")
    assert not is_not_numeric_or_period("9")
    assert is_not_numeric_or_period("+")
    assert not any([is_not_numeric_or_period(v) for v in "......."])


def test_sum_part_numbers():
    schematic = Schematic.parse([line.strip() for line in PART_1_RAW])
    assert sum_part_numbers(schematic) == 4361


def test_sum_gear_ratios():
    schematic = Schematic.parse([line.strip() for line in PART_1_RAW])
    assert sum_gear_ratios(schematic) == 467835
