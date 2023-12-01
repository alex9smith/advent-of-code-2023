from day_01 import (
    remove_letters,
    get_first_last,
    replace_spelled_with_digits,
    sum_calibration_values,
    search_for_first_spelled_digit,
    SearchResult,
)

FIXTURES = [
    ("1abc2", "12", 12),
    ("pqr3stu8vwx", "38", 38),
    ("a1b2c3d4e5f", "12345", 15),
    ("treb7uchet", "7", 77),
]

PART_2_FIXTURES = [
    ("two1nine", "t2o1n9e", 29),
    ("eightwothree", "e8t2ot3e", 83),
    ("abcone2threexyz", "abco1e2t3exyz", 13),
    ("xtwone3four", "xt2o1e3f4r", 24),
    ("4nineeightseven2", "4n9ee8ts7n2", 42),
    ("zoneight234", "zo1e8t234", 14),
    ("7pqrstsixteen", "7pqrsts6xteen", 76),
    ("eighthree", "e8t3e", 83),
    ("sevenine", "s7n9e", 79),
]


def test_search_for_first_spelled_digit():
    assert search_for_first_spelled_digit("eightwothree") == SearchResult(True, "eight")
    assert search_for_first_spelled_digit("8wo3") == SearchResult(False, "")


def test_replace_spelled_with_digits():
    for input, output, _ in PART_2_FIXTURES:
        assert output == replace_spelled_with_digits(input)


def test_remove_letters():
    for input, output, _ in FIXTURES:
        assert str(output) == remove_letters(input)


def test_get_first_last():
    for input, _, output in FIXTURES:
        assert output == get_first_last(remove_letters(input))


def test_sum_calibration_values():
    # part 1
    FIXTURE_SUM = sum(i for _, _, i in FIXTURES)
    assert FIXTURE_SUM == sum_calibration_values([l for l, _, _ in FIXTURES])

    # part 2
    PART_2_FIXTURE_SUM = sum(i for _, _, i in PART_2_FIXTURES)
    assert PART_2_FIXTURE_SUM == sum_calibration_values(
        [replace_spelled_with_digits(l) for l, _, _ in PART_2_FIXTURES]
    )
