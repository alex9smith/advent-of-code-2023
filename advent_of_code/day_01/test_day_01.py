from day_01 import remove_letters, get_first_last, sum_calibration_values

FIXTURES = [
    ("1abc2", "12", 12),
    ("pqr3stu8vwx", "38", 38),
    ("a1b2c3d4e5f", "12345", 15),
    ("treb7uchet", "7", 77),
]


def test_remove_letters():
    for input, output, _ in FIXTURES:
        assert str(output) == remove_letters(input)


def test_get_first_last():
    for input, _, output in FIXTURES:
        assert output == get_first_last(remove_letters(input))


def test_sum_calibration_values():
    FIXTURE_SUM = sum(i for _, _, i in FIXTURES)
    assert FIXTURE_SUM == sum_calibration_values([l for l, _, _ in FIXTURES])
