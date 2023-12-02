from day_02 import (
    handful_power,
    parse_handfuls,
    Handful,
    Game,
    is_possible_handful,
    parse_line,
    sum_possible_game_ids,
)

PART_1_FIXTURE = [
    "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
    "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
    "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
    "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
    "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green",
]


def test_parse_handfuls():
    assert parse_handfuls("3 blue, 4 red") == [Handful(4, 3, 0)]
    assert parse_handfuls(" 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green") == [
        Handful(4, 3, 0),
        Handful(1, 6, 2),
        Handful(0, 0, 2),
    ]


def test_is_possible_handful():
    assert is_possible_handful(Handful(1, 2, 3))
    assert not is_possible_handful(Handful(500, 3, 4))
    assert not is_possible_handful(Handful(1, 500, 4))
    assert not is_possible_handful(Handful(2, 2, 500))


def test_parse_line():
    game = parse_line("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green")
    assert game.id == 1
    assert game.handfuls == [
        Handful(4, 3, 0),
        Handful(1, 6, 2),
        Handful(0, 0, 2),
    ]


def test_game_possible():
    assert Game(
        1,
        [
            Handful(4, 3, 0),
            Handful(1, 6, 2),
            Handful(0, 0, 2),
        ],
    ).is_possible()

    assert not Game(
        1,
        [
            Handful(1000, 3, 0),
        ],
    ).is_possible()


def test_sum_possible_games():
    assert sum_possible_game_ids(PART_1_FIXTURE) == 8


def test_game_minimum_handful():
    game = Game(
        1,
        [
            Handful(4, 3, 0),
            Handful(1, 6, 2),
            Handful(0, 0, 2),
        ],
    )
    assert game.minimum_handful() == Handful(4, 6, 2)


def test_handful_power():
    assert handful_power(Handful(4, 6, 2)) == 48
