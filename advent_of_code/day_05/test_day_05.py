from day_05 import Almanac, map_from_search, SEED_TO_SOIL, safe_get_from_map
from pytest import fixture

INPUT = """
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""

EXPECTED = {50 + i: 52 + i for i in range(48)}
EXPECTED.update({98 + i: 50 + i for i in range(2)})

MAP = map_from_search(SEED_TO_SOIL.search(INPUT))


def test_map_from_search():
    assert map_from_search(None) == {}
    assert MAP == EXPECTED


def test_safe_get_from_map():
    assert safe_get_from_map(MAP, 50) == 52
    assert safe_get_from_map(MAP, 1) == 1


class TestAlmanac:
    @fixture
    def almanac(self) -> Almanac:
        return Almanac.from_input(INPUT)

    def test_from_input_seeds(self, almanac: Almanac):
        assert almanac.seeds == [79, 14, 55, 13]

    def test_from_input_map(self, almanac: Almanac):
        assert almanac.seed_to_soil == MAP

    def test_locations(self, almanac: Almanac):
        assert min(almanac.locations()) == 35
