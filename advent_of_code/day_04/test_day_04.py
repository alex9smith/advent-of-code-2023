from pytest import fixture
from day_04 import Card, sum_card_scores

FIXTURE = [
    "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53",
    "Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19",
    "Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1",
    "Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83",
    "Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36",
    "Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11",
]

CARD_SCORES = [8, 2, 2, 1, 0, 0]


class TestCard:
    @fixture
    def card(self) -> Card:
        return Card.from_line(FIXTURE[0])

    def test_from_line(self, card: Card):
        assert card.id == 1
        assert card.numbers == set([41, 48, 83, 86, 17])
        assert card.winners == set([83, 86, 6, 31, 17, 9, 48, 53])

    def test_score(self, card: Card):
        assert card.score() == 8

        for line, score in zip(FIXTURE, CARD_SCORES):
            card = Card.from_line(line)
            assert card.score() == score


def test_sum_card_scores():
    assert sum_card_scores(FIXTURE) == 13
