from dataclasses import dataclass
from typing import List
from math import prod


@dataclass
class Race:
    duration: int
    distance: int


def parse(input: str) -> List[Race]:
    lines = [line for line in input.split("\n") if line]
    time, distance = lines
    times = [int(t.strip()) for t in time.split()[1:] if not t.isspace()]
    distances = [int(d.strip()) for d in distance.split()[1:] if not d.isspace()]

    races = []
    for time, distance in zip(times, distances):
        races.append(Race(duration=time, distance=distance))

    return races


def total_distance(hold_time: int, race_duration: int):
    if hold_time >= race_duration:
        return 0

    return hold_time * (race_duration - hold_time)


def ways_to_win(race: Race) -> int:
    """
    6, 7 -> 3 -- interval 2 - 4
    7, 9 -> 4 -- interval 2 - 5
    15, 40 -> 8 -- interval 4 - 11
    30, 200 -> 9 -- interval 11 - 19
    """

    hold_time = 0
    for hold_time in range(race.duration):
        if total_distance(hold_time, race.duration) > race.distance:
            break

    midpoint = race.duration // 2
    pairs_further = midpoint - hold_time
    return (pairs_further * 2) + (1 if race.duration % 2 == 0 else 2)


def parse_ignoring_spaces(input: str) -> Race:
    lines = [line for line in input.split("\n") if line]
    time, distance = lines

    time = int("".join(time.replace("Time:", "").split()))
    distance = int("".join(distance.replace("Distance:", "").split()))

    return Race(duration=time, distance=distance)


if __name__ == "__main__":
    with open("./advent_of_code/day_06/day_06.txt", "r") as file:
        RAW = file.read()

    print("part 1")
    print(prod([ways_to_win(race) for race in parse(RAW)]))

    print("part 2")
    print(ways_to_win(parse_ignoring_spaces(RAW)))
