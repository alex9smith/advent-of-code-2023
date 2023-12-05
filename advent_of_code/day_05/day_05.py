from dataclasses import dataclass
from typing import Dict, List

import re

type Map = Dict[int, int]

SEEDS = re.compile(r"seeds: ((?:\d+( |\n))+)")
SEED_TO_SOIL = re.compile(r"seed-to-soil map:\n((\d+(?: |\n))+)")
SOIL_TO_FERTILIZER = re.compile(r"soil-to-fertilizer map:\n((\d+(?: |\n))+)")
FERTILIZER_TO_WATER = re.compile(r"fertilizer-to-water map:\n((\d+(?: |\n))+)")
WATER_TO_LIGHT = re.compile(r"water-to-light map:\n((\d+(?: |\n))+)")
LIGHT_TO_TEMPERATURE = re.compile(r"light-to-temperature map:\n((\d+(?: |\n))+)")
TEMPERATURE_TO_HUMIDITY = re.compile(r"temperature-to-humidity map:\n((\d+(?: |\n))+)")
HUMIDITY_TO_LOCATION = re.compile(r"humidity-to-location map:\n((\d+(?: |\n))+)")


def map_from_search(search: re.Match | None) -> Map:
    if not search:
        return {}

    raw_lines = [
        line.split() for line in search.group(1).split("\n") if not line.isspace()
    ]

    lines = [line for line in raw_lines if line]

    keys = []
    values = []

    for destination, source, length in lines:
        for i in range(int(length)):
            keys.append(int(source) + i)
            values.append(int(destination) + i)

    return {k: v for k, v in zip(keys, values)}


def safe_get_from_map(map: Map, index: int) -> int:
    if index in map:
        return map[index]

    else:
        return index


@dataclass
class Almanac:
    seeds: List[int]
    seed_to_soil: Map
    soil_to_fertilizer: Map
    fertilizer_to_water: Map
    water_to_light: Map
    light_to_temperature: Map
    temperature_to_humidity: Map
    humidity_to_location: Map

    @classmethod
    def from_input(cls, input: str) -> "Almanac":
        # seeds
        seeds_search = SEEDS.search(input)
        seeds = [int(s) for s in seeds_search.group(1).split()] if seeds_search else []

        return Almanac(
            seeds=seeds,
            seed_to_soil=map_from_search(SEED_TO_SOIL.search(input)),
            soil_to_fertilizer=map_from_search(SOIL_TO_FERTILIZER.search(input)),
            fertilizer_to_water=map_from_search(FERTILIZER_TO_WATER.search(input)),
            water_to_light=map_from_search(WATER_TO_LIGHT.search(input)),
            light_to_temperature=map_from_search(LIGHT_TO_TEMPERATURE.search(input)),
            temperature_to_humidity=map_from_search(
                TEMPERATURE_TO_HUMIDITY.search(input)
            ),
            humidity_to_location=map_from_search(HUMIDITY_TO_LOCATION.search(input)),
        )

    def locations(self) -> List[int]:
        locations = []

        for seed in self.seeds:
            locations.append(
                safe_get_from_map(
                    self.humidity_to_location,
                    safe_get_from_map(
                        self.temperature_to_humidity,
                        safe_get_from_map(
                            self.light_to_temperature,
                            safe_get_from_map(
                                self.water_to_light,
                                safe_get_from_map(
                                    self.fertilizer_to_water,
                                    safe_get_from_map(
                                        self.soil_to_fertilizer,
                                        safe_get_from_map(self.seed_to_soil, seed),
                                    ),
                                ),
                            ),
                        ),
                    ),
                )
            )

        return locations


if __name__ == "__main__":
    with open("./advent_of_code/day_05/day_05.txt", "r") as file:
        almanac = Almanac.from_input(file.read())

    print("part 1")
    print(min(almanac.locations()))
