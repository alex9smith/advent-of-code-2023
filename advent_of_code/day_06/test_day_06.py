from day_06 import parse, Race, total_distance, ways_to_win, parse_ignoring_spaces

INPUT = """
Time:      7  15   30
Distance:  9  40  200
"""


def test_parse():
    races = parse(INPUT)
    assert races[0] == Race(7, 9)
    assert races[1] == Race(15, 40)
    assert races[2] == Race(30, 200)


EXPECTED_DISTANCES_7 = [
    (0, 0),
    (1, 6),
    (2, 10),
    (3, 12),
    (4, 12),
    (5, 10),
    (6, 6),
    (0, 0),
]

EXPECTED_DISTANCES_6 = [(0, 0), (1, 5), (2, 8), (3, 9), (4, 8), (5, 5), (6, 0)]


def test_total_distance():
    for hold_time, expected in EXPECTED_DISTANCES_7:
        assert total_distance(hold_time=hold_time, race_duration=7) == expected

    for hold_time, expected in EXPECTED_DISTANCES_6:
        assert total_distance(hold_time=hold_time, race_duration=6) == expected


def test_ways_to_win():
    assert ways_to_win(Race(7, 9)) == 4
    assert ways_to_win(Race(15, 40)) == 8
    assert ways_to_win(Race(30, 200)) == 9


def test_parse_ignoring_spaces():
    assert parse_ignoring_spaces(INPUT) == Race(71530, 940200)
