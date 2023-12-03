from typing import List
from dataclasses import dataclass


type Row = List[str]


@dataclass
class Position:
    row: int
    start: int
    end: int

    def position_above(self) -> "Position":
        return Position(row=self.row - 1, start=self.start - 1, end=self.end + 1)

    def position_below(self) -> "Position":
        return Position(row=self.row + 1, start=self.start - 1, end=self.end + 1)


def is_not_numeric_or_period(input: str) -> bool:
    return not ((input.isnumeric()) or (input == "."))


@dataclass
class Schematic:
    rows: int
    columns: int
    data: List[Row]

    @classmethod
    def parse(cls, data: List[str]) -> "Schematic":
        separated = [list(line) for line in data]
        return Schematic(data=separated, rows=len(separated), columns=len(separated[0]))

    def find_all_numbers(self) -> List[Position]:
        in_number = False
        numbers: List[Position] = []
        for row_index, row in enumerate(self.data):
            start = 0
            for column_index, item in enumerate(row):
                if item.isnumeric():
                    if not in_number:
                        # Found the start of a new number
                        start = column_index
                        in_number = True

                elif in_number:
                    # Found the end of a number
                    numbers.append(Position(row_index, start, column_index - 1))
                    in_number = False

            # At the end of a row, if we're in a number then end it
            if in_number:
                numbers.append(Position(row_index, start, len(row)))
                in_number = False

        return numbers

    def get_valid_values_for_position(self, position: Position) -> str:
        if position.row < 0 or position.row > self.rows - 1:
            return ""

        start, end = position.start, position.end

        return "".join(self.data[position.row][max(start, 0) : min(end + 1, self.rows)])

    def is_position_part_number(self, position: Position) -> bool:
        surrounding: List[Position] = [
            # before
            Position(position.row, position.start - 1, position.start - 1),
            # after
            Position(position.row, position.end + 1, position.end + 1),
        ]
        if position.row == 0:
            # on the first row
            surrounding.append(position.position_below())

        elif position.row == self.rows - 1:
            # on the last row
            surrounding.append(position.position_above())
        else:
            # in the middle
            surrounding.append(position.position_above())
            surrounding.append(position.position_below())

        values = "".join(self.get_valid_values_for_position(p) for p in surrounding)
        return any([is_not_numeric_or_period(v) for v in values])


def sum_part_numbers(schematic: Schematic) -> int:
    numbers = schematic.find_all_numbers()
    part_numbers = [
        schematic.get_valid_values_for_position(p)
        for p in numbers
        if schematic.is_position_part_number(p)
    ]
    return sum([int(n) for n in part_numbers])


if __name__ == "__main__":
    with open("./advent_of_code/day_03/day_03.txt", "r") as file:
        lines = [line.strip() for line in file.readlines()]

    schematic = Schematic.parse(lines)

    print("part 1")
    print(sum_part_numbers(schematic))
