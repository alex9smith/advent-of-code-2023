from day00 import fibonacci

from pytest import raises


def test_validates_first_second():
    with raises(ValueError):
        fibonacci(5, 1, 0)


def test_validates_terms():
    with raises(ValueError):
        fibonacci(1, 2, -1)


def test_returns_first_with_one_term():
    first = 1
    assert [first] == fibonacci(first, 2, 1)


def test_returns_first_and_second_with_two_terms():
    first = 1
    second = 2
    assert [first, second] == fibonacci(first, second, 2)


def test_calculates_multiple_terms():
    assert [1, 2, 3, 5, 8] == fibonacci(1, 2, 5)
