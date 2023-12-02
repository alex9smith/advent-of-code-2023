from dataclasses import dataclass
from collections import namedtuple
from typing import List
import re

MAX_RED = 12
MAX_BLUE = 14
MAX_GREEN = 13

MATCH_GAME_ID = re.compile(r"Game (\d+): ")
MATCH_RED = re.compile(r"(\d+) red")
MATCH_BLUE = re.compile(r"(\d+) blue")
MATCH_GREEN = re.compile(r"(\d+) green")

type Line = str

Handful = namedtuple("Handful", "red, blue, green")


@dataclass
class Game:
    id: int
    handfuls: List[Handful]

    def is_possible(self) -> bool:
        return all(is_possible_handful(h) for h in self.handfuls)

    def minimum_handful(self) -> Handful:
        if len(self.handfuls) == 0:
            return Handful(0, 0, 0)

        max_red = max(h.red for h in self.handfuls)
        max_blue = max(h.blue for h in self.handfuls)
        max_green = max(h.green for h in self.handfuls)

        return Handful(max_red, max_blue, max_green)


def parse_handfuls(line: Line) -> List[Handful]:
    handfuls = []
    parts = [p.strip() for p in line.split(";")]
    for part in parts:
        red = 0
        blue = 0
        green = 0
        red_search = re.search(MATCH_RED, part)
        if red_search:
            red = int(red_search.group(1))

        blue_search = re.search(MATCH_BLUE, part)
        if blue_search:
            blue = int(blue_search.group(1))

        green_search = re.search(MATCH_GREEN, part)
        if green_search:
            green = int(green_search.group(1))

        handfuls.append(Handful(red, blue, green))
    return handfuls


def is_possible_handful(handful: Handful) -> bool:
    return (
        (handful.red <= MAX_RED)
        & (handful.blue <= MAX_BLUE)
        & (handful.green <= MAX_GREEN)
    )


def parse_line(line: Line) -> Game:
    id_search = re.search(MATCH_GAME_ID, line)

    if id_search:
        game_id = int(id_search.group(1))

        handfuls = parse_handfuls(line.replace(id_search.group(0), ""))

        return Game(game_id, handfuls)

    raise ValueError("No game found" + line)


def sum_possible_game_ids(lines: List[Line]) -> int:
    games = [parse_line(l) for l in lines]
    return sum(g.id for g in games if g.is_possible())


def handful_power(handful: Handful) -> int:
    return handful.red * handful.blue * handful.green


def sum_minimum_handful_powers(lines: List[Line]) -> int:
    games = [parse_line(l) for l in lines]
    minimum_handfuls = [g.minimum_handful() for g in games]
    return sum(handful_power(h) for h in minimum_handfuls)


if __name__ == "__main__":
    with open("./advent_of_code/day_02/day_02.txt", "r") as file:
        lines = [line.strip() for line in file.readlines()]

    print("part 1")
    print(sum_possible_game_ids(lines))

    print("part 2")
    print(sum_minimum_handful_powers(lines))
