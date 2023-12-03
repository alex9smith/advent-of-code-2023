from typing import List
from dataclasses import dataclass


type Row = List[str]


@dataclass(frozen=True)
class Position:
    row: int
    start: int
    end: int

    def position_above(self) -> "Position":
        return Position(row=self.row - 1, start=self.start - 1, end=self.end + 1)

    def position_below(self) -> "Position":
        return Position(row=self.row + 1, start=self.start - 1, end=self.end + 1)

    def contains(self, other: "Position") -> bool:
        # true if other is completely contained in self
        if self.row == other.row:
            if other.start >= self.start:
                if other.end <= self.end:
                    return True

        return False

    def separate(self) -> List["Position"]:
        return [Position(self.row, i, i) for i in range(self.start, self.end + 1)]


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

    def find_all_gears(self) -> List[Position]:
        gears = []
        for row_index, row in enumerate(self.data):
            for column_index, item in enumerate(row):
                if item == "*":
                    gears.append(Position(row_index, column_index, column_index))

        return gears

    def get_adjacent_positions(self, position: Position) -> List[Position]:
        start_of_row = position.start == 0
        end_of_row = position.end == self.columns - 1
        first_row = position.row == 0
        last_row = position.row == self.rows - 1

        left = 0 if start_of_row else position.start - 1
        right = position.end if end_of_row else position.end + 1

        positions = []

        # above and below
        if first_row:
            for p in Position(position.row + 1, left, right).separate():
                positions.append(p)

        elif last_row:
            for p in Position(position.row - 1, left, right).separate():
                positions.append(p)

        else:
            for p in Position(position.row + 1, left, right).separate():
                positions.append(p)
            for p in Position(position.row - 1, left, right).separate():
                positions.append(p)

        # sides
        positions.append(Position(position.row, left, left))
        positions.append(Position(position.row, right, right))

        return positions


def sum_part_numbers(schematic: Schematic) -> int:
    numbers = schematic.find_all_numbers()
    part_numbers = [
        schematic.get_valid_values_for_position(p)
        for p in numbers
        if schematic.is_position_part_number(p)
    ]
    return sum([int(n) for n in part_numbers])


def sum_gear_ratios(schematic: Schematic) -> int:
    potential_gears = schematic.find_all_gears()
    numbers = schematic.find_all_numbers()

    power = 0
    for gear in potential_gears:
        adjacent = schematic.get_adjacent_positions(gear)

        overlapping = list(set([n for n in numbers for a in adjacent if n.contains(a)]))
        if len(overlapping) == 2:
            power += int(schematic.get_valid_values_for_position(overlapping[0])) * int(
                schematic.get_valid_values_for_position(overlapping[1])
            )

    return power


if __name__ == "__main__":
    with open("./advent_of_code/day_03/day_03.txt", "r") as file:
        lines = [line.strip() for line in file.readlines()]

    schematic = Schematic.parse(lines)

    print("part 1")
    print(sum_part_numbers(schematic))

    print("part 2")
    print(sum_gear_ratios(schematic))
